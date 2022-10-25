# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel(briegel@mpia.de)
# @Date: 2022-04-06
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


from logging import DEBUG
from copy import deepcopy

from types import SimpleNamespace as sn

from datetime import datetime

from sdsstools.logger import StreamFormatter  
from sdsstools import get_logger, read_yaml_file
from sdsstools.logger import SDSSLogger

import aio_pika as apika

from clu import AMQPActor
from clu.client import AMQPReply

from cluplus.configloader import Loader

from lvmtel import __version__
from lvmtel.actor.commands import parser as command_parser

class LvmtelActor(AMQPActor):
    """Lvmtel base actor."""

    parser=command_parser

    def __init__(
        self,
        config, 
        *args,
        simulate:bool=False,
        **kwargs,
    ):   

        super().__init__(*args, **kwargs)

        #TODO: fix schema
        self.schema = {
                       "type": "object",
                       "properties": {
                            "temperature": {"type": "number"},
                            "humidity": {"type": "number"},
                            "pressure": {"type": "number"},
                      },
                      "additionalProperties": False,
        }

        if kwargs['verbose']:
            self.log.sh.setLevel(DEBUG)
            self.log.sh.formatter = StreamFormatter(fmt='%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)d: \033[1m%(message)s\033[21m') 


    async def start(self):
        """Start actor"""
        await super().start()

        self.load_schema(self.schema, is_file=False)
 
        self.log.debug("Start done")
        
    async def stop(self):
        """Stop actor and remove cameras."""
        await super().stop()




    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from hierachical configuration file(s)."""

        instance = super(LvmtelActor, cls).from_config(config, version=__version__, loader=Loader, *args, **kwargs)

        if kwargs["verbose"]:
            instance.log.fh.setLevel(DEBUG)
            instance.log.sh.setLevel(DEBUG)

        return instance
