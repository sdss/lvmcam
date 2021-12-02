#!/usr/bin/env python3

"""
Python3 class to work with Aravis/GenICam cameras, subclass of sdss-basecam.
.. module:: araviscam
.. moduleauthor:: Richard J. Mathar <mathar@mpia.de>
"""

import sys
import math
import asyncio
import numpy
import astropy

from basecam.mixins import ImageAreaMixIn
from basecam import (
    CameraSystem,
    BaseCamera,
    CameraEvent,
    CameraConnectionError,
    models,
    ExposureError,
)

from lvmcam.actor import modules


# Since the aravis wrapper for GenICam cameras (such as the Blackfly)
# is using glib2 GObjects to represent cameras and streams, the
# PyGObject module allows to call the C functions of aravis in python.
# https://pygobject.readthedocs.io/en/latest/
from lvmcam.araviscam.aravis import Aravis

import basecam.models.card as card

from lvmcam.actor.commands import expose

# https://pypi.org/project/sdss-basecam/
# https://githum.com/sdss/basecam/

# from sdsstools import read_yaml_file

__all__ = ["BlackflyCameraSystem", "BlackflyCamera", "BlackflyImageAreaMixIn"]


class BlackflyCameraSystem(CameraSystem):
    """A collection of GenICam cameras, possibly online
    :param camera_class : `.BaseCamera` subclass
        The subclass of `.BaseCamera` to use with this camera system.
    :param camera_config :
        A dictionary with the configuration parameters for the multiple
        cameras that can be present in the system, or the path to a YAML file.
        Refer to the documentation for details on the accepted format.
    :type camera_config : dict or path
    :param include : List of camera UIDs that can be connected.
    :type include : list
    :param exclude : list
        List of camera UIDs that will be ignored.
    :param logger : ~logging.Logger
        The logger instance to use. If `None`, a new logger will be created.
    :param log_header : A string to be prefixed to each message logged.
    :type log_header : str
    :param log_file : The path to which to log.
    :type log_file : str
    :param verbose : Whether to log to stdout.
    :type verbose : bool
    :param ip_list: A list of IP-Adresses to be checked/pinged.
    :type ip_list: List of strings.
    """

    __version__ = "0.0.301"

    # A list of ip addresses in the usual "xxx.yyy.zzz.ttt" or "name.subnet.net"
    # format that have been added manually/explicitly and may not be found by the
    # usual broadcase auto-detection (i.e., possibly on some other global network).
    ips_nonlocal = []

    def __init__(
        self,
        camera_class=None,
        camera_config=None,
        include=None,
        exclude=None,
        logger=None,
        log_header=None,
        log_file=None,
        verbose=False,
        ip_list=None,
    ):
        super().__init__(
            camera_class=camera_class,
            camera_config=camera_config,
            include=include,
            exclude=exclude,
            logger=logger,
            log_header=log_header,
            log_file=log_file,
            verbose=verbose,
        )

        # If the ctor is fed with an explicit list of IP addresses, add them to
        # the scanner (with delayed inspection in list_available_cameras).
        if ip_list is not None:
            self.ips_nonlocal.extend(ip_list)

        # debuging: print yaml configuration
        # print(self._config)

    # @modules.timeit
    def list_available_cameras(self):
        """Gather serial numbers of online Aravis/Genicam devices.
        :return: a list of serial numbers (as strings). This list may be
                 empty if no cameras are online/switched on.
                 For cameras explicitly addressed by IP, the serial
                 numbers have the format sn@ip, with an @ between number and address.
        :rtype: list

        .. todo:: optionally implement a specific filter for Blackfly's if Basler
                  cameras should not be listed.
        """

        # Start with (pessimistic) initially empty set of online devices
        serialNums = []
        addrs = []

        # Broadcast ethernet/bus for recognized cameras.
        # Warning/todo: this gathers also cameras that are not of the Blackfly class,
        # and in conjunction with the SDSS may also recognize the Basler cameras..
        Aravis.update_device_list()
        Ndev = Aravis.get_n_devices()
        # print(str(Ndev) + " cameras online")

        # get_device_id returns a string of type, SN, MAC etc
        for i in range(Ndev):
            cam = Aravis.Camera.new(Aravis.get_device_id(i))
            uid = cam.get_string("DeviceSerialNumber")
            serialNums.append(uid)
            addrs.append("")

        # Try to ping cameras explicitly proposed with ctor.
        for ip in self.ips_nonlocal:
            try:
                cam = Aravis.Camera.new(ip)
                uid = cam.get_string("DeviceSerialNumber")
                # If is this was already in the scan: discard, else add
                if uid not in serialNums:
                    serialNums.append(uid)
                    addrs.append("@" + ip)
            except:
                # apparently no such camera at this address....
                pass

        # we zip the two lists to the format 'serialnumber{@ip}'
        ids = []
        for cam in range(len(serialNums)):
            ids.append(serialNums[cam] + addrs[cam])

        return ids

from basecam.models.builtin import basic_fz_fits_model


class BlackflyCamera(BaseCamera):
    """A FLIR (formerly Point Grey Research) Blackfly camera.
    Given the pixel scale on the benches of LVMi and the assumption
    of 9 um pixel sizes of the LVMi cameras, we assume that the
    cameras have roughly 1 arsec per pixel, so they are used without binning.

    In addition we let the camera flip the standard image orientation of the data
    values assuming that values are stored into a FITS interface (where
    the first values in the sequential data are the bottom row).
    So this is not done in this python code but by the camera.
    """
    
    # fits_model=basic_fz_fits_model

    def __init__(
        self,
        uid,
        camera_system,
        name=None,
        force=False,
        image_namer=None,
        camera_params={},
    ):
        super().__init__(
            uid=uid,
            camera_system=camera_system,
            name=name,
            force=force,
            image_namer=image_namer,
            camera_params=camera_params,
        )
        self.header = []

    @modules.atimeit
    async def _connect_internal(self, **kwargs):
        """Connect to a camera and upload basic binning and ROI parameters.
        :param kwargs:  recognizes the key uid with integer value, the serial number
                        If the key uid is absent, tries to attach to the first camera.
                        This is a subdictionary of 'cameras' in practise.
        """

        # print(self.name)
        # search for an optional uid key in the arguments
        try:
            uid = kwargs["uid"]
        except:
            uid = None

        # reverse lookup of the uid in the list of known cameras
        cs = BlackflyCameraSystem(BlackflyCamera)
        slist = cs.list_available_cameras()

        if uid is None:
            # uid was not specified: grab the first device that is found
            # print("no uid provided, attaching to first camera")
            idx = 0
        else:
            # print("searching " + uid + " in " + str(slist) )
            idx = -1
            for id in slist:
                # remove the optional ip address of the id
                slistuid = id.split("@")[0]
                if slistuid == uid:
                    idx = slist.index(id)
            # not found
            if idx < 0:
                raise CameraConnectionError("SN " + uid + " not connected")

        cam = None
        try:
            if "@" in slist[idx]:
                # if the camera was not on local network use the address part
                cam = Aravis.Camera.new(slist[idx].split("@")[1])
            else:
                # otherwise the index is the same as the search order...
                cam = Aravis.Camera.new(Aravis.get_device_id(idx))
        except:
            raise CameraConnectionError(" not connected")

        # search for an optional gain key in the arguments
        # todo: one could interpret gain=0 here as to call set_gain_auto(ARV_AUTO_ON)
        try:
            gain = kwargs["gain"]
            if gain > 0.0:
                # todo: it might make sense to squeeze this into the minimum
                # and maximum range of the camera's gain if outside that range.
                self.device.set_gain_auto(0)
                cam.set_gain(gain)
        except Exception as ex:
            # print("failed to set gain " + str(ex))
            pass

        # see arvenums.h for the list of pixel formats. This is MONO_16 here, always
        cam.set_pixel_format(0x01100007)

        # search for an optional x and y binning factor
        try:
            var = kwargs["binning"]
            cam.set_binning(var[0], var[1])
        except Exception as ex:
            # print("failed to set binning " + str(ex))
            # horizontal and vertical binning set to 1
            cam.set_binning(1, 1)

        # scan the general list of genicam featured values
        # of the four native types
        for typp, arvLst in kwargs.items():
            if arvLst is not None:
                if typp == "bool":
                    for genkey, genval in arvLst.items():
                        try:
                            cam.set_boolean(genkey, int(genval))
                        except:
                            # probably a typo in the yaml file... todo: log this
                            # print("failed for " + str(genkey)+str(genval))
                            pass
                elif typp == "int":
                    for genkey, genval in arvLst.items():
                        try:
                            cam.set_integer(genkey, genval)
                        except:
                            # probably a typo in the yaml file... todo: log this
                            # print("failed for " + str(genkey)+str(genval))
                            pass
                elif typp == "float":
                    for genkey, genval in arvLst.items():
                        try:
                            cam.set_float(genkey, genval)
                        except:
                            # probably a typo in the yaml file... todo: log this
                            # print("failed for " + str(genkey)+str(genval))
                            pass
                elif typp == "string":
                    for genkey, genval in arvLst.items():
                        try:
                            cam.set_string(genkey, genval)
                        except:
                            # probably a typo in the yaml file... todo: log this
                            # print("failed for " + str(genkey)+str(genval))
                            pass

        dev = cam.get_device()

        # Take full frames by default (maximizing probability of LVM guide camera
        # to find guide stars in the field)
        roiBounds = [-1, -1]
        try:
            roiBounds[0] = dev.get_integer_feature_value("WidthMax")
            roiBounds[1] = dev.get_integer_feature_value("HeightMax")
            # print(" ROI " + str(roiBounds[0]) + " x " + str(roiBounds[1]) )
            cam.set_region(0, 0, roiBounds[0], roiBounds[1])
        except Exception as ex:
            # print("failed to set ROI " + str(ex))
            pass

        self.device = cam
        self.regionBounds = roiBounds

    @modules.atimeit
    async def _disconnect_internal(self):
        """Close connection to camera."""
        self.device = None

    # @modules.atimeit
    async def _expose_grabFrame(self, exposure):
        """Read a single unbinned full frame.
        The class splits the parent class' exposure into this function and
        the part which generates the FITS file, because applications in guiders
        are usually only interested in the frame's data, and would not
        take the detour of generating a FITS file and reading it back from
        disk.

        :param exposure:  On entry, exposure.exptim is the intended exposure time in [sec]
                          On exit, exposure.data is the numpy array of the 16bit data
                          arranged in FITS order (i.e., the data of the bottom row appear first...)
        :return: The dictionary with the window location and size (x=,y=,width=,height=)
        """
        # To avoid being left over by other programs with no change
        # to set the exposure time, we switch the auto=0=off first
        self.device.set_exposure_time_auto(0)
        # Aravis assumes exptime in micro second integers
        exptime_ms = int(0.5 + exposure.exptime * 1e6)
        self.device.set_exposure_time(exptime_ms)

        # timeout (factor 2: assuming there may be two frames in auto mode taken
        #   internally)
        #   And 5 seconds margin for any sort of transmission overhead over PoE
        tout_ms = int(1.0e6 * (2.0 * exposure.exptime + 5))
        self.notify(CameraEvent.EXPOSURE_INTEGRATING)

        # the buffer allocated/created within the acquisition()
        buf = await self.loop.run_in_executor(None, self.device.acquisition, tout_ms)
        if buf is None:
            raise ExposureError(
                "Exposing for "
                + str(exposure.exptime)
                + " sec failed. Timout "
                + str(tout_ms / 1.0e6)
            )

        # Decipher which methods this aravis buffer has...
        # print(dir(buf))

        # reg becomes a x=, y=, width= height= dictionary
        # these are in standard X11 coordinates where upper left =(0,0)
        reg = buf.get_image_region()
        # print('region',reg)

        data = buf.get_data()

        exposure.data = numpy.ndarray(
            buffer=data, dtype=numpy.uint16, shape=(1, reg.height, reg.width)
        )
        # print("exposure data shape", exposure.data.shape)
        return reg

    @modules.atimeit
    async def _expose_internal(self, exposure):
        """Read a single unbinned full frame and store in a FITS file.
        :param exposure:  On entry exposure.exptim is the intended exposure time in [sec]
                  On exit, exposure.data contains the 16bit data of a single frame
        :return: There is no return value
        """

        # fill exposure.data with the frame's 16bit data
        # reg becomes a x=, y=, width= height= dictionary
        # these are in standard X11 coordinates where upper left =(0,0)

        reg = await self._expose_grabFrame(exposure)
        # print('region',reg)

        binxy = {}
        try:
            # becomes a dictionary with dx=... dy=... for the 2 horiz/vert binn fact
            binxy = self.device.get_binning()
        except Exception as ex:
            binxy = None

        # append FITS header cards
        # For the x/y coordinates transform from X11 to FITS coordinates
        # Todo: reports the camera y-flipped reg.y if ReversY=true above??
        addHeaders = [
            ("BinX", binxy.dx, "[ct] Horizontal Bin Factor 1, 2 or 4"),
            ("BinY", binxy.dy, "[ct] Vertical Bin Factor 1, 2 or 4"),
            ("Width", reg.width, "[ct] Pixel Columns"),
            ("Height", reg.height, "[ct] Pixel Rows"),
            ("RegX", 1 + reg.x, "[ct] Pixel Region Horiz start"),
            # The lower left FITS corner is the upper left X11 corner...
            (
                "RegY",
                self.regionBounds[1] - (reg.y + reg.height - 1),
                "[ct] Pixel Region Vert start",
            ),
        ]

        dev = self.device.get_device()
        # print(dir(dev))
        # print(dir(self))
        # print(self.camera_system.get_camera(self.name))
        # print(self.camera_system._config[self.name])

        try:
            gain = dev.get_float_feature_value("Gain")
            addHeaders.append(("Gain", gain, "Gain"))
        except Exception as ex:
            # print("failed to read gain" + str(ex))
            pass

        imgrev = [False, False]
        try:
            imgrev[0] = self.device.get_boolean("ReverseX")
            addHeaders.append(("ReverseX", imgrev[0] != 0, " Flipped left-right"))
            imgrev[1] = self.device.get_boolean("ReverseY")
            addHeaders.append(("ReverseY", imgrev[1] != 0, " Flipped up-down"))
            # print("reversed" +  str(imgrev[0]) + str(imgrev[1]) )
        except Exception as ex:
            # print("failed to read ReversXY" + str(ex))
            pass

        # This is an enumeration in the GenICam. See features list of
        #  `arv-tool-0.8 --address=192.168.70.50 features`

        binMod = [-1, -1]
        try:
            binMod[0] = dev.get_integer_feature_value("BinningHorizontalMode")
            if binMod[0] == 0:
                addHeaders.append(
                    ("BinModeX", "Averag", "Horiz Bin Mode Sum or Averag")
                )
            else:
                addHeaders.append(("BinModeX", "Sum", "Horiz Bin Mode Sum or Averag"))
            binMod[1] = dev.get_integer_feature_value("BinningVerticalMode")
            if binMod[1] == 0:
                addHeaders.append(("BinModeY", "Averag", "Vert Bin Mode Sum or Averag"))
            else:
                addHeaders.append(("BinModeY", "Sum", "Vert Bin Mode Sum or Averag"))
        except Exception as ex:
            # print("failed to read binmode" + str(ex))
            pass

        tmp = False
        try:
            tmp = self.device.get_boolean("BlackLevelClampingEnable")
            addHeaders.append(
                ("CAMBLCLM", tmp != 0, "Black Level Clamping en/disabled")
            )
            # print("BlackLevelClampingEnable" +  str(imgrev[0]) + str(imgrev[1]) )
        except Exception as ex:
            # print("failed to read BlackLevelClampingEnable" + str(ex))
            pass

        try:
            camtyp = self.device.get_model_name()
            addHeaders.append(("CAMTYP", camtyp, "Camera model"))
        except:
            pass

        # call _expose_wcs() to gather WCS header keywords
        addHeaders.extend(self._expose_wcs(exposure, reg))

        # for headr in addHeaders:
        #     exposure.fits_model[0].header_model.append(models.Card(headr))

        self.header = addHeaders
        # print(repr(exposure.to_hdu()[0].header))

        # unref() is currently usupported in this GObject library.
        # Hope that this does not lead to any memory leak....
        # buf.unref()
        return

    # @modules.timeit
    def _expose_wcs(self, exposure, reg):
        """Gather information for the WCS FITS keywords
        :param exposure:  On entry exposure.exptim is the intended exposure time in [sec]
                  On exit, exposure.data contains the 16bit data of a single frame
        :param reg The binning and region information
        """
        # the section/dictionary of the yaml file for this camera
        yamlconfig = self.camera_system._config[self.name]
        wcsHeaders = []

        # The distance from the long edge of the FLIR camera to the center
        # of the focus (fiber) is 7.144+4.0 mm according to SDSS-V_0110 figure 6
        # and 11.14471 according to figure 3-1 of LVMi-0081
        # For the *w or *e cameras the pixel row 1 (in FITS) is that far
        # away in the y-coordinate and in the middle of the x-coordinate.
        # For the *c cameras at the fiber bundle we assume them to be in the beam center.
        wcsHeaders.append(("CRPIX1", reg.width / 2, "[px] RA center along axis 1"))
        if self.name[-1] == "c":
            wcsHeaders.append(
                ("CRPIX2", reg.height / 2, "[px] DEC center along axis 2")
            )
        else:
            # convert 11.14471 mm to microns and to to pixels
            crefy = 11.14471 * 1000.0 / yamlconfig["pixsize"]
            wcsHeaders.append(("CRPIX2", -crefy, "[px] DEC center along axis 2"))

        return wcsHeaders


class BlackflyImageAreaMixIn(ImageAreaMixIn):
    """Allows to select image region and binning factors"""

    async def _get_image_area_internal(self):
        pass

    async def _set_image_area_internal(self, area=None):
        pass

    async def _get_binning_internal(self):
        pass

    async def _set_binning_internal(self, hbin, vbin):
        pass


# async def singleFrame(
#     exptim,
#     name,
#     verb=False,
#     ip_add=None,
#     config="cameras.yaml",
#     targ=None,
#     kmirr=0.0,
#     flen=None,
# ):
#     """Expose once and write the image to a FITS file.
#     :param exptim: The exposure time in seconds. Non-negative.
#     :type exptim: float
#     :param verb: Verbosity on or off
#     :type verb: boolean
#     :param ip_add: list of explicit IP's (like 192.168.70.51 or lvmt.irws2.mpia.de)
#     :type ip_add: list of strings
#     :param config: Name of the YAML file with the cameras configuration
#     :type config: string of the file name
#     :param targ: alpha/delta ra/dec of the sidereal target
#     :type targ: astropy.coordinates.SkyCoord
#     :param kmirr: Kmirr angle in degrees (0 if up, positive with right hand rule along North on bench)
#     :type kmirr: float
#     :param flen: focal length of telescope/siderostat in mm
#                  If not provided it will be taken from the configuration file
#     :type flen: float
#     """

#     cs = BlackflyCameraSystem(
#         BlackflyCamera, camera_config=config, verbose=verb, ip_list=ip_add
#     )
#     cam = await cs.add_camera(name=name)
#     # print("cameras", cs.cameras)
#     # print("config" ,config)

#     exp = await cam.expose(exptim, "LAB TEST")

#     if targ is not None and kmirr is not None:
#         # if there is already a (partial) header information, keep it,
#         # otherwise create one ab ovo.
#         if exp.wcs is None:
#             wcshdr = astropy.io.fits.Header()
#         else:
#             wcshdr = exp.wcs.to_header()

#         key = astropy.io.fits.Card("CUNIT1", "deg", "WCS units along axis 1")
#         wcshdr.append(key)
#         key = astropy.io.fits.Card("CUNIT2", "deg", "WCS units along axis 2")
#         wcshdr.append(key)
#         key = astropy.io.fits.Card("CTYPE1", "RA---TAN", "WCS type axis 1")
#         wcshdr.append(key)
#         key = astropy.io.fits.Card("CTYPE2", "DEC--TAN", "WCS type axis 2")
#         wcshdr.append(key)
#         key = astropy.io.fits.Card("CRVAL1", targ.ra.deg, "[deg] RA at reference pixel")
#         wcshdr.append(key)
#         key = astropy.io.fits.Card(
#             "CRVAL2", targ.dec.deg, "[deg] DEC at reference pixel"
#         )
#         wcshdr.append(key)

#         # field angle: degrees, then radians
#         # direction of NCP on the detectors (where we have already flipped pixels
#         # on all detectors so fieldrot=kmirr=0 implies North is up and East is left)
#         # With right-handed-rule: zero if N=up (y-axis), 90 deg if N=right (x-axis)
#         # so the direction is the vector ( sin(f), cos(f)) before the K-mirror.
#         # Action of K-mirror is ( cos(2*m), sin(2*m); sin(2*m), -cos(2*m))
#         # and action of prism is (-1 0 ; 0 1), i.e. to flip the horizontal coordinate.
#         # todo: get starting  value from a siderostat field rotation tracking model
#         fieldrot = 0.0

#         if name[-1] == "c":
#             # without prism, assuming center camera placed horizontally
#             if name[:4] == "spec":
#                 # without K-mirror
#                 pass
#             else:
#                 # with K-mirror
#                 # in the configuration the y-axis of the image has been flipped,
#                 # the combined action of (1, 0; 0, -1) and the K-mirror is (cos(2m), sin(2m); -sin(2m), cos(2m))
#                 # and applied to the input vector this is (sin(2m+f), cos(2m+f))
#                 fieldrot += 2.0 * kmirr
#         else:
#             # with prism
#             if name[:4] == "spec":
#                 # without K-mirror
#                 # Applied to input beam this gives (-sin(f), cos(f)) but prism effect
#                 # had been undone by vertical flip in the FLIR image.
#                 pass
#             else:
#                 # with K-mirror
#                 # Combined action of K-mirror and prism is (-cos(2*m), -sin(2*m);sin(2*m), -cos(2*m)).
#                 # Applied to input beam this gives (-sin(2*m+f), -cos(2*m+f)) = (sin(2*m+f+pi), cos(2*m+f+pi)).
#                 fieldrot += 2.0 * kmirr + 180.0

#             if name[-1] == "w":
#                 # Camera is vertically,
#                 # so up in the lab is right in the image
#                 fieldrot += 90
#             else:
#                 # Camera is vertically,
#                 # so up in the lab is left in the image
#                 fieldrot -= 90

#         fieldrot = math.radians(fieldrot)

#         # the section/dictionary of the yaml file for this camera
#         yamlconfig = cs._config[name]

#         if flen is None:
#             flen = yamlconfig["flen"]

#         # pixel scale per arcseconds is focal length *pi/180 /3600
#         # = flen * mm *pi/180 /3600
#         # = flen * um *pi/180 /3.6, so in microns per arcsec...
#         pixscal = math.radians(flen) / 3.6

#         # degrees per pixel is arcseconds per pixel/3600 = (mu/pix)/(mu/arcsec)/3600
#         degperpix = yamlconfig["pixsize"] / pixscal / 3600.0

#         # for the right handed coordinates
#         # (pixx,pixy) = (cos f', -sin f'; sin f', cos f')*(DEC,RA) where f' =90deg -fieldrot
#         # (pixx,pixy) = (sin f, -cos f; cos f , sin f)*(DEC,RA)
#         # (sin f, cos f; -cos f, sin f)*(pixx,pixy) = (DEC,RA)
#         # (-cos f, sin f; sin f, cos f)*(pixx,pixy) = (RA,DEC)
#         # Note that the det of the WCS matrix is negativ (because RA/DEC is left-handed...)
#         cosperpix = degperpix * math.cos(fieldrot)
#         sinperpix = degperpix * math.sin(fieldrot)
#         key = astropy.io.fits.Card("CD1_1", -cosperpix, "[deg/px] WCS matrix diagonal")
#         wcshdr.append(key)
#         key = astropy.io.fits.Card("CD2_2", cosperpix, "[deg/px] WCS matrix diagonal")
#         wcshdr.append(key)
#         key = astropy.io.fits.Card(
#             "CD1_2", sinperpix, "[deg/px] WCS matrix outer diagonal"
#         )
#         wcshdr.append(key)
#         key = astropy.io.fits.Card(
#             "CD2_1", sinperpix, "[deg/px] WCS matrix outer diagonal"
#         )
#         wcshdr.append(key)

#         exp.wcs = astropy.wcs.WCS(wcshdr)
#         # print(exp.wcs.to_header_string())
#         for headr in wcshdr.cards:
#             exp.fits_model[0].header_model.append(models.Card(headr))

#     await exp.write()
#     if verb:
#         print("wrote ", exp.filename)


# # A debugging aid, demonstrator and simple test run
# # This allows to call this file as an executable from the command line.
# # The last command line argument must be the name of the camera
# # as used in the configuration file.
# # Example
# #    BlackflyCam.py [-e seconds] [-v] [-c ../etc/cameras.yaml] [-r 2h10m10s] [-d -20d10m3s]
# #       [-K kmirrdegrees] [-s "LCO"|"MPIA"|"APO"|"KHU"] [-f focallengthmm] {spec.age|spec.agw|...}
# if __name__ == "__main__":

#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-e",
#         "--exptime",
#         type=float,
#         default=5.0,
#         help="Expose for for exptime seconds",
#     )

#     parser.add_argument(
#         "-v", "--verbose", action="store_true", help="print some notes to stdout"
#     )

#     # With the -i switch we can add an explicit IP-Adress for a
#     # camera if we want to read a camera that is not reachable
#     # by the broadcast scanner.
#     parser.add_argument("-i", "--ip", help="IP address of camera")

#     # Name of an optional YAML file
#     parser.add_argument(
#         "-c", "--cfg", default="cameras.yaml", help="YAML file of lvmt cameras"
#     )

#     # right ascension in degrees
#     parser.add_argument("-r", "--ra", help="RA J2000 in degrees or in xxhxxmxxs format")

#     # declination in degrees
#     parser.add_argument(
#         "-d", "--dec", help="DEC J2000 in degrees or in +-xxdxxmxxs format"
#     )

#     # K-mirror angle in degrees
#     # Note this is only relevant for 3 of the 4 tables/telescopes
#     parser.add_argument("-K", "--Kmirr", type=float, help="K-mirror angle in degrees")

#     # focal length of telescope in mm
#     # Default is the LCO triple lens configuration of 1.8 meters
#     parser.add_argument(
#         "-f", "--flen", type=float, default=1839.8, help="focal length in mm"
#     )

#     # shortcut for site coordinates: observatory
#     # parser.add_argument("-s", '--site', default="LCO", help="LCO or MPIA or APO or KHU")

#     # the last argument is mandatory: must be the name of exactly one camera
#     # as used in the configuration file
#     parser.add_argument("camname", default="sci.agw")

#     args = parser.parse_args()

#     ip_cmdLine = []
#     if args.ip is not None:
#         ip_cmdLine.append(args.ip)

#     # check ranges and combine ra/dec into a single SkyCoord
#     if args.ra is not None and args.dec is not None:
#         if args.ra.find("h") < 0:
#             # apparently simple floating point representation
#             targ = astropy.coordinates.SkyCoord(
#                 ra=float(args.ra), dec=float(args.dec), unit="deg"
#             )
#         else:
#             targ = astropy.coordinates.SkyCoord(args.ra + " " + args.dec)
#     else:
#         targ = None

#     # print(targ)

#     # The following 2 lines test that listing the connected cameras works...
#     # bsys = BlackflyCameraSystem(camera_class=BlackflyCamera)
#     # bsys.list_available_cameras()

#     asyncio.run(
#         singleFrame(
#             args.exptime,
#             args.camname,
#             verb=args.verbose,
#             ip_add=ip_cmdLine,
#             config=args.cfg,
#             targ=targ,
#             kmirr=args.Kmirr,
#             flen=args.flen,
#         )
#     )


class WcsHdrCards(card.MacroCard):
    def macro(self, exposure, context={}):
        wcshdr = get_wcshdr(modules.variables.cs_list[0], modules.variables.camname, modules.variables.targ, modules.variables.kmirr, modules.variables.flen)
        return wcshdr

# @modules.timeit
def get_wcshdr(
    cs,
    name,
    targ,
    kmirr,
    flen,
):
    if targ is not None and kmirr is not None:
        # wcshdr = astropy.io.fits.Header()
        wcshdr = []

        key = astropy.io.fits.Card("CUNIT1", "deg", "WCS units along axis 1")
        wcshdr.append(key)
        key = astropy.io.fits.Card("CUNIT2", "deg", "WCS units along axis 2")
        wcshdr.append(key)
        key = astropy.io.fits.Card("CTYPE1", "RA---TAN", "WCS type axis 1")
        wcshdr.append(key)
        key = astropy.io.fits.Card("CTYPE2", "DEC--TAN", "WCS type axis 2")
        wcshdr.append(key)
        key = astropy.io.fits.Card("CRVAL1", targ.ra.deg, "[deg] RA at reference pixel")
        wcshdr.append(key)
        key = astropy.io.fits.Card(
            "CRVAL2", targ.dec.deg, "[deg] DEC at reference pixel"
        )
        wcshdr.append(key)

        # field angle: degrees, then radians
        # direction of NCP on the detectors (where we have already flipped pixels
        # on all detectors so fieldrot=kmirr=0 implies North is up and East is left)
        # With right-handed-rule: zero if N=up (y-axis), 90 deg if N=right (x-axis)
        # so the direction is the vector ( sin(f), cos(f)) before the K-mirror.
        # Action of K-mirror is ( cos(2*m), sin(2*m); sin(2*m), -cos(2*m))
        # and action of prism is (-1 0 ; 0 1), i.e. to flip the horizontal coordinate.
        # todo: get starting  value from a siderostat field rotation tracking model
        fieldrot = 0.0

        if name[-1] == "c":
            # without prism, assuming center camera placed horizontally
            if name[:4] == "spec":
                # without K-mirror
                pass
            else:
                # with K-mirror
                # in the configuration the y-axis of the image has been flipped,
                # the combined action of (1, 0; 0, -1) and the K-mirror is (cos(2m), sin(2m); -sin(2m), cos(2m))
                # and applied to the input vector this is (sin(2m+f), cos(2m+f))
                fieldrot += 2.0 * kmirr
        else:
            # with prism
            if name[:4] == "spec":
                # without K-mirror
                # Applied to input beam this gives (-sin(f), cos(f)) but prism effect
                # had been undone by vertical flip in the FLIR image.
                pass
            else:
                # with K-mirror
                # Combined action of K-mirror and prism is (-cos(2*m), -sin(2*m);sin(2*m), -cos(2*m)).
                # Applied to input beam this gives (-sin(2*m+f), -cos(2*m+f)) = (sin(2*m+f+pi), cos(2*m+f+pi)).
                fieldrot += 2.0 * kmirr + 180.0

            if name[-1] == "w":
                # Camera is vertically,
                # so up in the lab is right in the image
                fieldrot += 90
            else:
                # Camera is vertically,
                # so up in the lab is left in the image
                fieldrot -= 90

        fieldrot = math.radians(fieldrot)

        # the section/dictionary of the yaml file for this camera
        yamlconfig = cs._config[name]

        if flen is None:
            flen = yamlconfig["flen"]

        # pixel scale per arcseconds is focal length *pi/180 /3600
        # = flen * mm *pi/180 /3600
        # = flen * um *pi/180 /3.6, so in microns per arcsec...
        pixscal = math.radians(flen) / 3.6

        # degrees per pixel is arcseconds per pixel/3600 = (mu/pix)/(mu/arcsec)/3600
        degperpix = yamlconfig["pixsize"] / pixscal / 3600.0

        # for the right handed coordinates
        # (pixx,pixy) = (cos f', -sin f'; sin f', cos f')*(DEC,RA) where f' =90deg -fieldrot
        # (pixx,pixy) = (sin f, -cos f; cos f , sin f)*(DEC,RA)
        # (sin f, cos f; -cos f, sin f)*(pixx,pixy) = (DEC,RA)
        # (-cos f, sin f; sin f, cos f)*(pixx,pixy) = (RA,DEC)
        # Note that the det of the WCS matrix is negativ (because RA/DEC is left-handed...)
        cosperpix = degperpix * math.cos(fieldrot)
        sinperpix = degperpix * math.sin(fieldrot)
        key = astropy.io.fits.Card("CD1_1", -cosperpix, "[deg/px] WCS matrix diagonal")
        wcshdr.append(key)
        key = astropy.io.fits.Card("CD2_2", cosperpix, "[deg/px] WCS matrix diagonal")
        wcshdr.append(key)
        key = astropy.io.fits.Card(
            "CD1_2", sinperpix, "[deg/px] WCS matrix outer diagonal"
        )
        wcshdr.append(key)
        key = astropy.io.fits.Card(
            "CD2_1", sinperpix, "[deg/px] WCS matrix outer diagonal"
        )
        wcshdr.append(key)
        return wcshdr
    else:
        return None
