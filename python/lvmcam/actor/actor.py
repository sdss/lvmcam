# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel(briegel@mpia.de)
# @Date: 2022-04-06
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


from logging import DEBUG

#from os.path import expandvars
from expandvars import expand as expandvars


from sdsstools.logger import StreamFormatter  
from sdsstools import get_logger, read_yaml_file
from sdsstools.logger import SDSSLogger

from clu import AMQPActor

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
        self.dirname = config_get(config, "dirname", None)
        self.basename = config_get(config, "basename", None)
        print(f'{config_get(config,"camtype", "skymakercam")}')
        camera_type = camera_types[config_get(config,"camtype", "skymakercam") if not simulate else "skymakercam"](config) 
        
        super().__init__(camera_type, *args, command_parser=camera_parser, version=__version__, **kwargs)

        self.exposure_state = {}

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

        #self.log.debug(str(self.model.schema))


    async def start(self):
        """Start actor and add cameras."""
        await super().start()

#        image_namer =  ImageNamerPlus(dirname="$HOME/{self.camera.name.replace('.', self.ospathsep)}/{date.strftime('%Y%m%d')}")

        for camera in self.camera_system._config:
            try:
                cam = await self.camera_system.add_camera(name=camera, uid=self.camera_system._config[camera]["uid"])
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
