# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel(briegel@mpia.de)
# @Date: 2022-04-06
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


from logging import DEBUG

from types import SimpleNamespace as sn

from datetime import datetime

from sdsstools.logger import StreamFormatter  
from sdsstools import get_logger, read_yaml_file
from sdsstools.logger import SDSSLogger

import aio_pika as apika


from clu import AMQPActor
from clu.client import AMQPReply

from cluplus.configloader import Loader

from basecam import BaseCamera
from basecam.actor import BaseCameraActor
from basecam.exposure import ImageNamer
from basecam.models import FITSModel, Extension, basic_header_model

from lvmcam import __version__
from lvmcam.actor.commands import camera_parser
#from lvmcam.model import fits_model, lvmcam_fz_fits_model
from lvmcam.models import CameraCards, WcsCards, ScraperParamCards, ScraperDataStore

from araviscam import BlackflyCameraSystem, BlackflyCamera
from skymakercam import SkymakerCameraSystem, SkymakerCamera


camera_types = {"araviscam": lambda *args, **kwargs: BlackflyCameraSystem(BlackflyCamera, *args, **kwargs ),
                "skymakercam": lambda *args, **kwargs: SkymakerCameraSystem(SkymakerCamera, *args, **kwargs)}


__all__ = ["LvmcamActor"]


def config_get(config, key, default=None):
    """ DOESNT work for keys with dots !!! """
    def g(config, key, d=None):
        k = key.split('.', maxsplit=1)
        c = config.get(k[0] if not k[0].isnumeric() else int(k[0]))  # keys can be numeric
        return d if c is None else c if len(k) < 2 else g(c, k[1], d) if type(c) is dict else d
    return g(config, key, default)



class LvmcamActor(BaseCameraActor, AMQPActor):
    """Lvmcam base actor."""

    def __init__(
        self,
        config, 
        *args,
        simulate:bool=False,
        **kwargs,
    ):   
        camera_type = camera_types[config_get(config,"camera_type", "skymakercam") if not simulate else "skymakercam"](config) 

        for cam, conf in config.get("cameras", {}).items():
            config["cameras"][cam] = {**config.get("camera_params", {}), **conf}

        super().__init__(camera_type, *args, command_parser=camera_parser, version=__version__, **kwargs)

        #TODO: fix schema
        self.schemaCamera = {
                       "type": "object",
                       "properties": {
                            "binning": {"type": "array"},
                            "area": {"type": "array"},
                        }
                  }

        self.schema = {
                    "type": "object",
                    "properties": {
                     },
                     "additionalProperties": False,
        }

        if kwargs['verbose']:
            self.log.sh.setLevel(DEBUG)
            self.log.sh.formatter = StreamFormatter(fmt='%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)d: \033[1m%(message)s\033[21m') 

        self.dirname = config_get(config, "dirname", None)
        self.basename = config_get(config, "basename", None)

        self.exposure_state = {}

        self.scraper_store = ScraperDataStore(config_get(config, "scraper", {}))

    async def start(self):
        """Start actor and add cameras."""
        await super().start()

        header_model = basic_header_model
        header_model.append(CameraCards)
        header_model.append(ScraperParamCards())
        header_model.append(WcsCards())

        for camera in self.camera_system._config:
            try:
                cam = await self.camera_system.add_camera(name=camera, actor=self, scraper_store=self.scraper_store)
                self.log.debug(f"camname {camera}")
                self.log.debug(f"basename {self.basename}")
                self.log.debug(f"dirname {self.dirname}")
                
                cam.image_namer = ImageNamer(basename=self.basename, dirname=self.dirname, camera=cam)
                cam.fits_model = FITSModel(
                    [
                        Extension(data="raw", 
                        header_model=header_model,
                        compressed=None,
                        name="PRIMARY")
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

        for camera in self.camera_system._config:
            cam = await self.camera_system.remove_camera(name=self.camera_system._config[camera]["uid"])
            
        self.log.debug("Stop done")


    async def handle_reply(self, message: apika.IncomingMessage) -> AMQPReply:
        """Handles a reply received from the exchange.
        """

        reply = AMQPReply(message, log=self.log)
        if reply.sender in self.scraper_store.actors() and reply.headers.get("message_code", None) in ":i":
            timestamp = apika.message.decode_timestamp(message.timestamp) if message.timestamp else datetime.utcnow()
            self.scraper_store.update_with_actor_key_maps(reply.sender, reply.body, timestamp)
#        self.log.debug(self.scraper_store.data)

        return reply


    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from hierachical configuration file(s)."""

        instance = super(LvmcamActor, cls).from_config(config, loader=Loader, *args, **kwargs)

        if kwargs["verbose"]:
            instance.log.fh.setLevel(DEBUG)
            instance.log.sh.setLevel(DEBUG)

        return instance
