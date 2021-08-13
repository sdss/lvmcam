#!/usr/bin/env python

"""
Python3 class to work with Aravis/GenICam cameras, subclass of sdss-basecam.
.. module:: araviscam
.. moduleauthor:: Richard J. Mathar <mathar@mpia.de>
"""

import sys
import asyncio
import numpy

from basecam.mixins import ImageAreaMixIn
from basecam import CameraSystem, BaseCamera, CameraEvent, CameraConnectionError, models

# Since the aravis wrapper for GenICam cameras (such as the Blackfly)
# is using glib2 GObjects to represent cameras and streams, the
# PyGObject module allows to call the C functions of aravis in python.
# https://pygobject.readthedocs.io/en/latest/
import gi
gi.require_version('Aravis', '0.8')
from gi.repository import Aravis


# https://pypi.org/project/sdss-basecam/
# https://githum.com/sdss/basecam/

# from sdsstools import read_yaml_file

__all__ = ['BlackflyCameraSystem', 'BlackflyCamera', 'BlackflyImageAreaMixIn']


class BlackflyCameraSystem(CameraSystem):
    """ A collection of GenICam cameras, possibly online
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

    __version__ = "0.0.138"

    # A list of ip addresses in the usual "xxx.yyy.zzz.ttt" or "name.subnet.net"
    # format that have been added manually/explicitly and may not be found by the
    # usual broadcase auto-detection (i.e., possibly on some other global network).
    ips_nonlocal = []

    def __init__(self, camera_class=None, camera_config=None,
                 include=None, exclude=None, logger=None,
                 log_header=None, log_file=None, verbose=False, ip_list=None):
        super().__init__(camera_class=camera_class, camera_config=camera_config,
                         include=include, exclude=exclude, logger=logger, log_header=log_header,
                         log_file=log_file, verbose=verbose)

        # If the ctor is fed with an explicit list of IP addresses, add them to
        # the scanner (with delayed inspection in list_available_cameras).
        if ip_list is not None:
            self.ips_nonlocal.extend(ip_list)

        # print(self._config)

    def list_available_cameras(self):
        """ Gather serial numbers of online Aravis/Genicam devices.
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
            addrs.append('')

        # Try to ping cameras explicitly proposed with ctor.
        for ip in self.ips_nonlocal:
            try:
                cam = Aravis.Camera.new(ip)
                uid = cam.get_string("DeviceSerialNumber")
                # If is this was already in the scan: discard, else add
                if uid not in serialNums:
                    serialNums.append(uid)
                    addrs.append('@'+ip)
            except:
                # apparently no such camera at this address....
                pass

        # we zip the two lists to the format 'serialnumber{@ip}'
        ids = []
        for cam in range(len(serialNums)):
            ids.append(serialNums[cam]+addrs[cam])

        return ids


class BlackflyCamera(BaseCamera):
    """ A FLIR (formerly Point Grey Research) Blackfly camera.
    Given the pixel scale on the benches of LVMi and the assumption
    of 9 um pixel sizes of the LVMi cameras, we assume that the
    cameras have roughly 1 arsec per pixel, so they are used without binning.

    In addition we let the camera flip the standard image orientation of the data
    values assuming that values are stored into a FITS interface (where
    the first values in the sequential data are the bottom row).
    So this is not done in this python code but by the camera.
    """

    async def _connect_internal(self, **kwargs):
        """Connect to a camera and upload basic binning and ROI parameters.
        :param kwargs:  recognizes the key uid with integer value, the serial number
                        If the key uid is absent, tries to attach to the first camera.
                        This is a subdictionary of 'cameras' in practise.
        """

        # search for an optional uid key in the arguments
        try:
            uid = kwargs['uid']
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
            gain = kwargs['gain']
            if gain > 0.0:
                # todo: it might make sense to squeeze this into the minimum
                # and maximum range of the camera's gain if outside that range.
                self.device.set_gain_auto(0)
                cam.set_gain(gain)
        except Exception as ex:
            # print("failed to set gain " + str(ex))
            pass

        # see arvenums.h for the list of pixel formats. This is MONO_16 here
        cam.set_pixel_format(0x01100007)

        # search for an optional x and y binning factor
        try:
            var = kwargs['binning']
            cam.set_binning(var[0], var[1])
        except Exception as ex:
            # print("failed to set binning " + str(ex))
            # horizontal and vertical binning set to 1
            cam.set_binning(1, 1)

        # scan the general list of genicam featured values
        # of the four native types
        for typp, arvLst in kwargs.items():
            if arvLst is not None:
                if typp == 'bool':
                    for genkey, genval in arvLst.items():
                        try:
                            cam.set_boolean(genkey, int(genval))
                        except:
                            # probably a typo in the yaml file... todo: log this
                            # print("failed for " + str(genkey)+str(genval))
                            pass
                elif typp == 'int':
                    for genkey, genval in arvLst.items():
                        try:
                            cam.set_integer(genkey, genval)
                        except:
                            # probably a typo in the yaml file... todo: log this
                            # print("failed for " + str(genkey)+str(genval))
                            pass
                elif typp == 'float':
                    for genkey, genval in arvLst.items():
                        try:
                            cam.set_float(genkey, genval)
                        except:
                            # probably a typo in the yaml file... todo: log this
                            # print("failed for " + str(genkey)+str(genval))
                            pass
                elif typp == 'string':
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

    async def _disconnect_internal(self):
        """Close connection to camera.
        """
        self.device = None

    async def _expose_grabFrame(self, exposure):
        """ Read a single unbinned full frame.
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
        tout_ms = int(1.0e6 * (2.*exposure.exptime+5))
        self.notify(CameraEvent.EXPOSURE_INTEGRATING)

        # the buffer allocated/created within the acquisition()
        buf = await self.loop.run_in_executor(None, self.device.acquisition, tout_ms)
        if buf is None:
            raise ExposureError("Exposing for " + str(exposure.exptime) +
                                " sec failed. Timout " + str(tout_ms/1.0e6))

        # Decipher which methods this aravis buffer has...
        # print(dir(buf))

        # reg becomes a x=, y=, width= height= dictionary
        # these are in standard X11 coordinates where upper left =(0,0)
        reg = buf.get_image_region()
        # print('region',reg)

        data = buf.get_data()

        exposure.data = numpy.ndarray(buffer=data, dtype=numpy.uint16,
                                      shape=(1, reg.height, reg.width))
        # print("exposure data shape", exposure.data.shape)

        return reg

    async def _expose_internal(self, exposure):
        """ Read a single unbinned full frame and store in a FITS file.
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
            ("RegX", 1+reg.x, "[ct] Pixel Region Horiz start"),
            # The lower left FITS corner is the upper left X11 corner...
            ("RegY", self.regionBounds[1]-(reg.y+reg.height-1),
             "[ct] Pixel Region Vert start")
        ]

        dev = self.device.get_device()
        # print(dir(dev))

        try:
            gain = dev.get_float_feature_value("Gain")
            addHeaders.append(("Gain", gain, "Gain"))
        except Exception as ex:
            # print("failed to read gain" + str(ex))
            pass

        imgrev = [False, False]
        try:
            imgrev[0] = self.device.get_boolean("ReverseX")
            addHeaders.append(
                ("ReverseX", imgrev[0] != 0, " Flipped left-right"))
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
                    ("BinModeX", "Averag", "Horiz Bin Mode Sum or Averag"))
            else:
                addHeaders.append(
                    ("BinModeX", "Sum", "Horiz Bin Mode Sum or Averag"))
            binMod[1] = dev.get_integer_feature_value("BinningVerticalMode")
            if binMod[1] == 0:
                addHeaders.append(
                    ("BinModeY", "Averag", "Vert Bin Mode Sum or Averag"))
            else:
                addHeaders.append(
                    ("BinModeY", "Sum", "Vert Bin Mode Sum or Averag"))
        except Exception as ex:
            # print("failed to read binmode" + str(ex))
            pass

        tmp = False
        try:
            tmp = self.device.get_boolean("BlackLevelClampingEnable")
            addHeaders.append(
                ("CAMBLCLM", tmp != 0, "Black Level Clamping en/disabled"))
            # print("BlackLevelClampingEnable" +  str(imgrev[0]) + str(imgrev[1]) )
        except Exception as ex:
            # print("failed to read BlackLevelClampingEnable" + str(ex))
            pass

        try:
            camtyp = self.device.get_model_name()
            addHeaders.append(("CAMTYP", camtyp, "Camera model"))
        except:
            pass

        for header in addHeaders:
            exposure.fits_model[0].header_model.append(models.Card(header))

        # unref() is currently usupported in this GObject library.
        # Hope that this does not lead to any memory leak....
        # buf.unref()
        return


class BlackflyImageAreaMixIn(ImageAreaMixIn):
    """ Allows to select image region and binning factors
    """
    async def _get_image_area_internal(self):
        pass

    async def _set_image_area_internal(self, area=None):
        pass

    async def _get_binning_internal(self):
        pass

    async def _set_binning_internal(self, hbin, vbin):
        pass


async def singleFrame(exptim, name, verb=False, ip_add=None, config="../etc/cameras.yaml"):
    """ Expose once and write the image to a FITS file.
    :param exptim: The exposure time in seconds. Non-negative.
    :type exptim: float
    :type exptim: float
    :param verb: Verbosity on or off
    :type verb: boolean
    :param ip_add: list of explicit IP's (like 192.168.70.51 or lvmt.irws2.mpia.de)
    :type ip_add: list of strings
    :param config: Name of the YAML file with the cameras configuration
    :type config: string of the file name
    """

    cs = BlackflyCameraSystem(
        BlackflyCamera, camera_config=config, verbose=verb, ip_list=ip_add)
    cam = await cs.add_camera(name=name, uid=cs._config['sci.agw']['uid'])
    # print("cameras", cs.cameras)
    # print("config" ,config)

    exp = await cam.expose(exptim, "LAB TEST")
    await cs.remove_camera(name=name, uid=cs._config['sci.agw']['uid'])
    await exp.write()
    if verb:
        print("wrote ", exp.filename)

# A debugging aid, demonstrator and simple test run
# This allows to call this file as an executable from the command line.
# The last command line argument must be the name of the camera
# as used in the configuration file.
# Example
#    BlackflyCam.py [-e seconds] [-v] [-c ../etc/cameras.yaml] {spec.age|spec.agw|...}
if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", '--exptime', type=float, default=5.0,
                        help="Expose for for exptime seconds")

    parser.add_argument("-v", '--verbose', action='store_true',
                        help="print some notes to stdout")

    # With the -i switch we can add an explicit IP-Adress for a
    # camera if we want to read a camera that is not reachable
    # by the broadcast scanner.
    parser.add_argument("-i", '--ip', help="IP address of camera")

    # Name of an optional YAML file
    parser.add_argument("-c", '--cfg', default="../etc/cameras.yaml",
                        help="YAML file of lvmt cameras")

    # the last argument is mandatory: must be the name of exactly one camera
    # as used in the configuration file
    parser.add_argument('camname', default="sci.agw")

    args = parser.parse_args()

    ip_cmdLine = []
    if args.ip is not None:
        ip_cmdLine.append(args.ip)

    # The following 2 lines test that listing the connected cameras works...
    # bsys = BlackflyCameraSystem(camera_class=BlackflyCamera)
    # bsys.list_available_cameras()

    asyncio.run(singleFrame(args.exptime, args.camname, 
                            verb=args.verbose, ip_add=ip_cmdLine, config=args.cfg))
