# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel(briegel@mpia.de)
# @Date: 2022-04-06
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


from logging import DEBUG

#from os.path import expandvars
from expandvars import expand as expandvars
from types import SimpleNamespace as sn

from datetime import datetime

from sdsstools.logger import StreamFormatter  
from sdsstools import get_logger, read_yaml_file
from sdsstools.logger import SDSSLogger

import aio_pika as apika

from clu import AMQPActor
from clu.client import AMQPReply

from basecam import BaseCamera
from basecam.actor import BaseCameraActor
from basecam.exposure import ImageNamer

from lvmcam import __version__
from lvmcam.actor.commands import camera_parser


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

        from sdsstools import get_logger
        logger = get_logger("test")
        
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
        
        self.scraper_map = config_get(config, "scraper", None)
        self.log.debug(str(self.scraper_map))
        self.scraper_actors = list(self.scraper_map.keys()) if self.scraper_map else None
        self.scraper_data = {}
        self.log.debug(str(self.scraper_map))


    async def start(self):
        """Start actor and add cameras."""
        await super().start()

#        image_namer =  ImageNamerPlus(dirname="$HOME/{self.camera.name.replace('.', self.ospathsep)}/{date.strftime('%Y%m%d')}")

        for camera in self.camera_system._config:
            try:
                self.log.debug(f"scraper data {self.scraper_data}")
                cam = await self.camera_system.add_camera(name=camera, actor=self, scraper_data=self.scraper_data)
                self.log.debug(f"camname {camera}")
                basename = expandvars(self.basename) if self.basename else "{camera.name}-{num:04d}.fits"
                self.log.debug(f"basename {basename}")
                dirname = expandvars(self.dirname) if self.dirname else "."
                self.log.debug(f"dirname {dirname}")
                
                cam.image_namer = ImageNamer(basename=basename, dirname=dirname, camera=cam)

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

        try:
            if message.timestamp:
                self.log.info(f"delay: {datetime.now() - apika.message.decode_timestamp(message.timestamp)} {apika.message.decode_timestamp(message.timestamp)} {message.timestamp}")
        except Exception as ex:
            self.log.error(f"{ex}")

        if reply.sender in self.scraper_actors and reply.headers.get("message_code", None) in ":i":
            # self.log.debug(f"{reply.sender}: {reply.body}")
            sender_map = self.scraper_map.get(reply.sender, None)
            timestamp = apika.message.decode_timestamp(message.timestamp) if message.timestamp else datetime.utcnow()
            # self.scraper_data = {**self.scraper_data, **{sender_map[k]:sn(val=v, ts=timestamp) for k, v in reply.body.items() if k in sender_map.keys()}}
            for k,v in {sender_map[k]:sn(val=v, ts=timestamp) for k, v in reply.body.items() if k in sender_map.keys()}.items():
                self.scraper_data[k]=v
#            self.log.debug(f"{self.scraper_data}")


        return reply

