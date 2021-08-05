from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from araviscam.araviscam import BlackflyCam
from clu.command import Command

from . import parser


#from araviscam import BlackflyCam as blc

# from lvmieb.controller.controller import IebController
# from lvmieb.exceptions import LvmIebError


__all__ = ["singleframe"]


@parser.group()
def singleframe(*args):
    """singleframe expose. fixed expose time (0.5sec) returns fits file"""

    pass


@singleframe.command()
# @click.option(
#   "-s",
#   "--side",
#   type=click.Choice(["all", "right", "left"]),
#   default = "all",
#   help="all, right, or left",
# )
@click.argument("EXPTIME", type=float) #capital letter
async def singleexpose(command: Command, exptime:float):
    await BlackflyCam.singleFrame(exptim=exptime,name="test")
    command.info("Exposing")
