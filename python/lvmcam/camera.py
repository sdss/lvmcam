#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Richard J. Mathar (mathar@mpia.de)
# @Filename: camera.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

# Since the aravis wrapper for GenICam cameras (such as the Blackfly)
# is using glib2 GObjects to represent cameras and streams, the
# PyGObject module allows to call the C functions of aravis in python.
# https://pygobject.readthedocs.io/en/latest/

from __future__ import annotations

import abc
import asyncio
import math
from collections import namedtuple
from logging import DEBUG

from typing import Any

import gi
import numpy

from basecam import BaseCamera, CameraEvent, CameraSystem, ExposureError
from basecam.mixins import CoolerMixIn, ExposureTypeMixIn, ImageAreaMixIn
from sdsstools.logger import StreamFormatter

from lvmcam import __version__ as lvmcam_version


gi.require_version("Aravis", "0.8")
from gi.repository import Aravis  # type: ignore  # noqa: E402


__all__ = ["BlackflyCameraSystem", "BlackflyCamera"]


class GainMixIn(object, metaclass=abc.ABCMeta):
    """A mixin that provides manual control over the camera gain."""

    @abc.abstractmethod
    async def _set_gain_internal(self, gain):
        """Internal method to set the gain."""

        raise NotImplementedError

    @abc.abstractmethod
    async def _get_gain_internal(self):
        """Internal method to get the gain."""

        raise NotImplementedError

    async def set_gain(self, gain):
        """Seta the  gain of the camera."""

        return await self._set_gain_internal(gain)

    async def get_gain(self):
        """Gets the gain of the camera."""

        return await self._get_gain_internal()


class BlackflyCameraSystem(CameraSystem):
    """A collection of GenICam cameras, possibly online.

    Parameters
    ----------
    camera_class : `.BaseCamera` subclass
        The subclass of `.BaseCamera` to use with this camera system.
    camera_config : dict or path
        A dictionary with the configuration parameters for the multiple
        cameras that can be present in the system, or the path to a YAML file.
        Refer to the documentation for details on the accepted format.
    include : list
        List of camera UIDs that can be connected.
    exclude : list
        List of camera UIDs that will be ignored.
    logger : ~logging.Logger
        The logger instance to use. If `None`, a new logger will be created.
    log_header : str
        A string to be prefixed to each message logged.
    log_file : str
        The path to which to log.
    verbose : bool
        Whether to log to stdout.

    """

    ## A list of ip addresses in the usual "xxx.yyy.zzz.ttt" or "name.subnet.net"
    ## format that have been added manually/explicitly and may not be found by the
    ## usual broadcase auto-detection (i.e., possibly on some other global network).
    # ips_nonlocal = []

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

    def list_available_cameras(self):
        return self.cameras

    @property
    def __version__(self):
        """Returns the version."""

        return lvmcam_version


Point = namedtuple("Point", ["x0", "y0"])
Size = namedtuple("Size", ["wd", "ht"])
Rect = namedtuple("Rect", ["x0", "y0", "wd", "ht"])


class BlackflyCamera(
    BaseCamera,
    ExposureTypeMixIn,
    ImageAreaMixIn,
    CoolerMixIn,
    GainMixIn,
):
    """A FLIR (formerly Point Grey Research) Blackfly camera.
    Given the pixel scale on the benches of LVMi and the assumption
    of 9 um pixel sizes of the LVMi cameras, we assume that the
    cameras have roughly 1 arsec per pixel, so they are used without binning.

    In addition we let the camera flip the standard image orientation of the data
    values assuming that values are stored into a FITS interface (where
    the first values in the sequential data are the bottom row).
    So this is not done in this python code but by the camera.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger.sh.setLevel(DEBUG)
        self.logger.sh.formatter = StreamFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s "
            "%(filename)s:%(lineno)d: \033[1m%(message)s\033[21m"
        )

        self.actor = self.camera_params.get("actor", None)

        self.gain = -1
        self.binning = [-1, -1]
        self.cam: Any = None
        self.cam_type = "unknown"
        self.temperature = -1
        self.camera_state: str = "idle"

        self.detector_size = Size(-1, -1)
        self.region_bounds = Size(-1, -1)
        self.image_area = Rect(-1, -1, -1, -1)

        self.pixsize = self.camera_params.get("pixsize", 0.0)
        self.flen = self.camera_params.get("flen", 0.0)
        self.telescope = self.camera_params.get("telescope", "NA")

        # pixel scale per arcseconds is focal length *pi/180 /3600
        # = flen * mm *pi/180 /3600
        # = flen * um *pi/180 /3.6, so in microns per arcsec...
        self.pixscale = math.radians(self.flen) / 3.6
        self.arcsec_per_pix = self.pixsize / self.pixscale
        self.log(f"arcsec_per_pix {self.arcsec_per_pix}")

        # degrees per pixel is arcseconds per pixel/3600 = (mu/pix)/(mu/arcsec)/3600
        self.degperpix = self.pixsize / self.pixscale / 3600.0

    async def _connect_internal(self, **kwargs):
        """Connect to a camera and upload basic binning and ROI parameters."""

        self.logger.debug(f"connect {self.name} {self.uid}")
        ip = self.camera_params.get("ip")

        self.logger.debug(f"{ip}")

        self.cam = Aravis.Camera.new(ip)
        self.cam_type = self.cam.get_model_name()
        self.logger.debug(f"{self.cam_type}")

        self.logger.debug(f"Pixsize: {self.pixsize}")

        self.arcsec_per_pix = self.pixsize / self.pixscale
        self.degperpix = self.arcsec_per_pix / 3600.0

        self.logger.debug(f"{self.cam.get_binning()}")

        try:
            await self.set_binning(1, 1)
        except Exception as ex:
            self.logger.warning(f"{ex}")
            await asyncio.sleep(5.0)
            self.logger.warning(f"{ex}")
            await self.set_binning(1, 1)

        self.detector_size = Size(
            self.cam.get_width_bounds().max,
            self.cam.get_height_bounds().max,
        )
        self.logger.debug(f"{self.detector_size}")

        # search for an optional gain key in the arguments
        # todo: one could interpret gain=0 here as to call set_gain_auto(ARV_AUTO_ON)
        await self.set_gain(self.camera_params.get("gain", 0))

        # search for an optional x and y binning factor,
        # fullframe image area will be set automatically with the binning.
        await self.set_binning(*self.camera_params.get("binning", [1, 1]))
        self.logger.debug(f"{self.image_area}")

        # see arvenums.h for the list of pixel formats. This is MONO_16 here, always
        self.cam.set_pixel_format(0x01100007)

        # scan the general list of genicam featured values
        # of the four native types
        for typp, arvLst in self.camera_params.get("genicam_params", {}).items():
            if arvLst is not None:
                if typp == "bool":
                    for genkey, genval in arvLst.items():
                        try:
                            if self.cam.get_boolean(genkey) != genval:
                                self.cam.set_boolean(genkey, int(genval))
                            self.logger.debug(f"genicam param : {genkey}={genval}")
                        except Exception as ex:
                            self.logger.error(f"failed setting: {genkey}={genval} {ex}")
                elif typp == "int":
                    for genkey, genval in arvLst.items():
                        try:
                            self.cam.set_integer(genkey, genval)
                            self.logger.debug(f"genicam param : {genkey}={genval}")
                        except Exception as ex:
                            self.logger.error(f"failed setting: {genkey}={genval} {ex}")
                elif typp == "float":
                    for genkey, genval in arvLst.items():
                        try:
                            self.cam.set_float(genkey, genval)
                            self.logger.debug(f"genicam param : {genkey}={genval}")
                        except Exception as ex:
                            self.logger.error(f"failed setting: {genkey}={genval} {ex}")
                elif typp == "string":
                    for genkey, genval in arvLst.items():
                        try:
                            self.logger.debug(f"genicam param : {genkey}={genval}")
                            self.cam.set_string(genkey, genval)
                        except Exception as ex:
                            self.logger.error(f"failed setting: {genkey}={genval} {ex}")

    async def _disconnect_internal(self):
        """Close connection to camera."""

        self.cam = None

    async def _expose_grabFrame(self, exposure, nretries=3):
        """Read a single unbinned full frame.

        The class splits the parent class' exposure into this function and
        the part which generates the FITS file, because applications in guiders
        are usually only interested in the frame's data, and would not
        take the detour of generating a FITS file and reading it back from
        disk.

        Parameters
        ----------
        exposure
            On entry, exposure.exptim is the intended exposure time in [sec]
            On exit, exposure.data is the numpy array of the 16bit data
            arranged in FITS order (i.e., the data of the bottom row appear first...)
        nretries
            Number of retries left. Sometimes the camera receives an empty buffer
            immediately after the acquisition begins; in this case we retry
            taking the image.

        Returns
        -------
        frame
            The dictionary with the window location and size (x=,y=,width=,height=)

        """

        # To avoid being left over by other programs with no change
        # to set the exposure time, we switch the auto=0=off first
        self.cam.set_exposure_time_auto(0)

        # Aravis assumes exptime in micro second integers
        exptime_ms = int(0.5 + exposure.exptime * 1e6)
        self.cam.set_exposure_time(exptime_ms)

        # timeout (factor 2: assuming there may be two frames in auto mode taken
        #   internally)
        #   And 5 seconds margin for any sort of transmission overhead over PoE
        tout_ms = int(1.0e6 * (2.0 * exposure.exptime + 5))
        self.notify(CameraEvent.EXPOSURE_INTEGRATING)

        # Wait a tiny bit for setting to take effect. This probably does not help
        # with the cases when the camera returns and empty buffer but ...
        await asyncio.sleep(0.1)

        # the buffer allocated/created within the acquisition()
        buf = await self.loop.run_in_executor(None, self.cam.acquisition, tout_ms)
        if buf is None:
            raise ExposureError(
                f"Exposing for {exposure.exptime} s failed. "
                f"Timed out {tout_ms / 1.0e6}."
            )

        roi = buf.get_image_region()
        if roi.width != self.image_area.wd or roi.height != self.image_area.ht:
            if nretries > 0:
                self.logger.warning(
                    f"Camera {self.name} returned an empty buffer. Retrying."
                )
                await asyncio.sleep(1)
                return await self._expose_grabFrame(exposure, nretries=nretries - 1)
            else:
                raise ExposureError(f"Camera {self.name} returned an empty buffer.")

        return buf.get_data(), roi

    async def expose(self, *args, **kwargs):
        exposure = await super().expose(*args, **kwargs)
        self.camera_state = "idle"

        return exposure

    async def _expose_internal(self, exposure, **kwargs):
        """Read a single full frame and store in a FITS file.

        Parameters
        ----------
        exposure
            On entry exposure.exptim is the intended exposure time in [sec]
            On exit, exposure.data contains the 16bit data of a single frame.

        """

        # fill exposure.data with the frame's 16bit data
        # reg becomes a x=, y=, width= height= dictionary
        # these are in standard X11 coordinates where upper left =(0,0)
        try:
            self.camera_state = "exposing"
            data, roi = await self._expose_grabFrame(exposure)

            self.logger.debug(f"{roi} {self.image_area}")

            exposure.data = numpy.ndarray(
                buffer=data,
                dtype=numpy.uint16,
                shape=(self.image_area.ht, self.image_area.wd),
            )
            self.temperature = await self.get_temperature()

        except Exception as err:
            # Sometimes the camera gets into read-only mode. In those cases
            # reconnecting seems to work. If that fails again, raise the error
            # but wrap it as an ExposureError so that the other camera does
            # not stop exposing.
            self.logger.warning(f"Camera replied with error: {err}")
            self.logger.warning("Will reconnect the camera and try again.")

            try:
                await self.reconnect()
                data, roi = await self._expose_grabFrame(exposure)
            except Exception as err:
                raise ExposureError(f"Camera failed to expose with error: {err}")
            finally:
                self.camera_state = "idle"

    async def reconnect(self):
        """Reconnects the camera."""

        await asyncio.wait_for(self.disconnect(), timeout=3)
        await asyncio.wait_for(self.connect(force=True), timeout=3)

    def _status_internal(self):
        return {
            "camera_state": self.camera_state,
            "temperature": self.cam.get_float("DeviceTemperature"),
            "cooler": math.nan,
        }

    async def _get_binning_internal(self):
        return list(self.cam.get_binning())

    async def _set_binning_internal(self, hbin, vbin):
        # search for an optional x and y binning factor
        try:
            self.logger.debug(f"set binning: {hbin} {vbin}")
            self.cam.set_binning(hbin, vbin)
            self.binning = [hbin, vbin]

        except Exception as ex:
            # horizontal and vertical binning set to 1
            self.logger.error(f"failed to set binning: {[hbin, vbin]}  {ex}")

        await self._set_image_area_internal()

    async def _get_image_area_internal(self):
        self.region_bounds = Size(
            self.cam.get_width_bounds().max,
            self.cam.get_height_bounds().max,
        )
        return self.region_bounds

    async def _set_image_area_internal(self, area=None):
        if area:
            self.logger.warning("image area only with fullframe")
            return
        await self._get_image_area_internal()
        self.cam.set_region(0, 0, *self.region_bounds)
        self.image_area = Rect(0, 0, *self.region_bounds)  # x0, y0, width, height

    async def _get_temperature_internal(self):
        self.temperature = self.cam.get_float("DeviceTemperature")
        return self.temperature

    async def _set_temperature_internal(self, temperature):
        self.logger.warning("temperature setting not possible")

    async def _set_gain_internal(self, gain):
        """Internal method to set the gain."""

        try:
            self.logger.debug(f"set gain: {self.camera_params.get('gain', None)}")
            if gain == 0.0:
                self.cam.set_gain_auto(1)
            else:
                self.cam.set_gain_auto(0)
                mn, mx = self.cam.get_gain_bounds()
                self.cam.set_gain(max(min(mx, gain), mn))
                self.gain = gain

        except Exception as ex:
            self.logger.error(f"failed to set gain: {gain} {ex}")

    async def _get_gain_internal(self):
        """Internal method to get the gain."""

        return self.camera_params.get("gain", None)
