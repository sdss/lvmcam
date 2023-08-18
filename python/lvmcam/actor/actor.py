#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-08-09
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import pathlib
from copy import deepcopy

from typing import Any

from astropy.coordinates import EarthLocation
from astropy.utils.iers import conf

from araviscam import BlackflyCamera, BlackflyCameraSystem
from basecam import ImageNamer
from basecam.actor import BaseCameraActor
from basecam.exposure import Exposure
from basecam.models import Extension, FITSModel, basic_header_model
from clu import AMQPActor, Command
from clu.client import AMQPReply
from sdsstools import read_yaml_file

from lvmcam import __version__
from lvmcam.models import CameraCards, GenicamCards, ScraperParamCards, WCSCards


conf.auto_download = False
conf.iers_degraded_accuracy = "ignore"


CWD = pathlib.Path(__file__).parents[1]
BASE_CAMERA_PARAMS = read_yaml_file(CWD / "etc/lvm.camera_param.agcam.yml")


def mergedicts(a, b):
    for key in b:
        if isinstance(a.get(key), dict) or isinstance(b.get(key), dict):
            mergedicts(a.get(key, {}), b.get(key, {}))
        else:
            a[key] = b[key]
    return a


def get_camera_class(config: dict):
    """Returns a camera class with the correct image namer and fits model."""

    dirname = config.get("dirname", ".")
    basename = config.get("basename", "{camera.name}-{num:04d}.fits")

    header_model = basic_header_model
    header_model.append(CameraCards)
    header_model.append(GenicamCards())
    header_model.append(ScraperParamCards())
    header_model.append(WCSCards())

    raw = Extension(
        data="raw",
        header_model=header_model,
        compressed="RICE_1",
        name="RAW",
    )

    class LVMCamera(BlackflyCamera):
        fits_model = FITSModel([raw])
        image_namer = ImageNamer(basename=basename, dirname=dirname)

        # LCO
        location = EarthLocation.from_geodetic(
            lon=-70.70166667,
            lat=-29.00333333,
            height=2282.0,
        )

        async def _expose_internal(self, exposure, **kwargs):
            exposure.obstime.location = self.location
            return await super()._expose_internal(exposure, **kwargs)

        async def expose(self, *args, **kwargs) -> Exposure:
            return await super().expose(*args, **kwargs)

    return LVMCamera


class LVMCamActor(BaseCameraActor, AMQPActor):
    """The LVMCam actor."""

    def __init__(self, *args, **kwargs):
        from lvmcam.actor.commands import camera_parser

        # Update camera config with default parameters.
        config = kwargs.get("config", {})

        for cam in config["cameras"]:
            camera_config = config["cameras"][cam]
            config["cameras"][cam] = mergedicts(camera_config, BASE_CAMERA_PARAMS)

        camera_class = get_camera_class(config)
        self.camera_system = BlackflyCameraSystem(camera_class, config["cameras"])

        super().__init__(
            self.camera_system,
            *args,
            version=__version__,
            command_parser=camera_parser,
            **kwargs,
        )

        if self.model:
            self.model.schema["additionalProperties"] = True

        # Scraped data from actors.
        self.scraper_data: dict[str, Any] = {}

        self.add_reply_callback(self.parse_actor_reply)

    async def start(self, **kwargs):
        """Starts the actor and adds cameras to the camera system."""

        assert isinstance(self.camera_system._config, dict)

        for camera in self.camera_system._config:
            try:
                cam = await self.camera_system.add_camera(name=camera, actor=self)
                self.log.debug(f"Camera {camera} connected")

                cam.fits_model.context.update({"__actor__": self})
            except Exception as ex:
                self.log.error(f"Camera {camera} failed connecting: {ex}")

        await super().start(**kwargs)

        for actor in self.config["scraper"]:
            await self.send_command(
                actor,
                "status",
                internal=True,
                await_command=False,
            )

        return self

    async def parse_actor_reply(self, reply: AMQPReply):
        """Parses replies from the actor system and updates scraped data."""

        scraper_defs: dict[str, dict[str, str]] = self.config["scraper"]
        if reply.sender not in scraper_defs or len(reply.body) == 0:
            return

        # Flatten body of the reply by dot-joining deeper dictionaries.
        # Do this until there are no more dictionaries.
        body = deepcopy(reply.body)

        while True:
            if not any([isinstance(value, dict) for value in body.values()]):
                break

            new_keys = {}
            remove_keys: list[str] = []
            for key, value in body.items():
                if isinstance(value, dict):
                    remove_keys.append(key)
                    for skey, svalue in body[key].items():
                        new_keys[key + "." + skey] = svalue

            for key in remove_keys:
                body.pop(key)

            body.update(new_keys)

        for key in scraper_defs[reply.sender]:
            if key in body:
                scraper_key = scraper_defs[reply.sender][key]
                self.scraper_data[scraper_key] = body[key]


LVMCamCommand = Command[LVMCamActor]
