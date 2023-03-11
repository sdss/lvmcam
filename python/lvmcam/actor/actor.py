# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel(briegel@mpia.de)
# @Date: 2022-04-06
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


from copy import deepcopy
from datetime import datetime
from logging import DEBUG

import aio_pika as apika
from astropy.utils import iers

from araviscam import BlackflyCamera, BlackflyCameraSystem
from basecam.actor import BaseCameraActor
from basecam.exposure import ImageNamer
from basecam.models import Extension, FITSModel, basic_header_model
from clu import AMQPActor
from clu.client import AMQPReply
from cluplus.configloader import Loader
from lvmtipo.ambient import Ambient
from lvmtipo.kmirror import Kmirror
from lvmtipo.siderostat import Siderostat
from lvmtipo.site import Site
from sdsstools.logger import StreamFormatter
from skymakercam import SkymakerCamera, SkymakerCameraSystem

from lvmcam import __version__
from lvmcam.actor.commands import camera_parser
from lvmcam.models import (
    CameraCards,
    GenicamCards,
    ScraperDataStore,
    ScraperParamCards,
    WcsCards,
)


iers.conf.auto_download = False


camera_types = {
    "araviscam": lambda *args, **kwargs: BlackflyCameraSystem(
        BlackflyCamera, *args, **kwargs
    ),
    "skymakercam": lambda *args, **kwargs: SkymakerCameraSystem(
        SkymakerCamera, *args, **kwargs
    ),
}


__all__ = ["LvmcamActor"]


class LvmcamActor(BaseCameraActor, AMQPActor):
    """Lvmcam base actor."""

    def __init__(
        self,
        config,
        *args,
        simulate: bool = False,
        **kwargs,
    ):
        self.camera_type = (
            config.get("camera_type", "skymakercam") if not simulate else "skymakercam"
        )

        def mergedicts(a, b):
            for key in b:
                if isinstance(a.get(key), dict) or isinstance(b.get(key), dict):
                    mergedicts(a[key], b[key])
                else:
                    a[key] = b[key]
            return a

        for cam, conf in config.get("cameras", {}).items():
            config["cameras"][cam] = mergedicts(
                deepcopy(config.get("camera_params", {})), {**conf}
            )

        super().__init__(
            camera_types[self.camera_type](config),
            *args,
            command_parser=camera_parser,
            version=__version__,
            **kwargs,
        )

        # TODO: fix schema
        self.schemaCamera = {
            "type": "object",
            "properties": {
                "state": {"type": "string"},
                "binning": {"type": "array"},
                "area": {"type": "array"},
            },
        }

        self.schema = {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        }

        if kwargs["verbose"]:
            self.log.sh.setLevel(DEBUG)
            self.log.sh.formatter = StreamFormatter(
                fmt="%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)d: "
                "\033[1m%(message)s\033[21m"
            )

        self.log.info(f"Camera type: {self.camera_type}")

        self.dirname = config.get("dirname", None)
        self.basename = config.get("basename", None)

        self.exposure_state = {}
        self.log.debug(f"{config.get('scraper', [])}")
        self.scraper_store = ScraperDataStore(self, config.get("scraper", {}))

        self.site = Site(name=config.get("site", "LCO"))
        self.log.info(f"Site: {config.get('site', 'LCO')}")

        # but south-> north at LCO
        if self.site.lat > 40.0:
            azang = 180  # MPIA
        else:
            azang = 0  # LCO, APO, KHU

        medSign = -1

        self.sid = Siderostat(azang=azang, medSign=medSign)
        self.ambi = Ambient()

        homeOffset = 135
        homeIsWest = False

        self.log.info(
            f"Site: {config.get('site', 'LCO')}, homeOffset: {homeOffset}, "
            f"homeIsWest: {homeIsWest}, azang: {azang}, medSign {medSign}"
        )

        self.kmirror = Kmirror(home_is_west=homeIsWest, home_offset=homeOffset)

    async def start(self):
        """Start actor and add cameras."""
        await super().start()

        header_model = basic_header_model
        header_model.append(CameraCards)
        if self.camera_type == "araviscam":
            header_model.append(GenicamCards())
        header_model.append(ScraperParamCards())
        header_model.append(WcsCards())

        for camera in self.camera_system._config:
            try:
                cam = await self.camera_system.add_camera(name=camera, actor=self)
                self.log.debug(f"camname {camera}")
                self.log.debug(f"basename {self.basename}")
                self.log.debug(f"dirname {self.dirname}")

                cam.image_namer = ImageNamer(
                    basename=self.basename, dirname=self.dirname, camera=cam
                )
                cam.fits_model = FITSModel(
                    [
                        Extension(
                            data="raw",
                            header_model=header_model,
                            compressed=None,
                            name="PRIMARY",
                        )
                    ]
                )
                cam.fits_model.context.update({"__actor__": self})

                self.schema["properties"][camera] = self.schemaCamera

            except Exception as ex:
                self.log.error(f"Camera {camera}: {ex}")

        self.load_schema(self.schema, is_file=False)

        self.log.debug("Start done")

    async def stop(self):
        """Stop actor and remove cameras."""
        await super().stop()

        self.log.debug("Stop done")

    async def handle_reply(self, message: apika.IncomingMessage) -> AMQPReply:
        """Handles a reply received from the exchange."""

        reply = await super().handle_reply(message)

        if (
            reply.sender in self.scraper_store.actors()
            and reply.headers.get("message_code", None) in ":i"
        ):
            timestamp = (
                apika.message.decode_timestamp(message.timestamp)
                if message.timestamp
                else datetime.utcnow()
            )

            self.scraper_store.update_with_actor_key_maps(
                reply.sender,
                reply.body,
                timestamp,
            )

        return reply

    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from hierachical configuration file(s)."""

        instance = super(LvmcamActor, cls).from_config(
            config,
            loader=Loader,
            *args,
            **kwargs,
        )

        if kwargs["verbose"]:
            instance.log.fh.setLevel(DEBUG)
            instance.log.sh.setLevel(DEBUG)

        return instance
