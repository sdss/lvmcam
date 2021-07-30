from __future__ import annotations, print_function, division, absolute_import

import asyncio
import click
from clu.command import Command
from lvmcam.flir import read_FLIR #auto run when actor started (30/07/21 Sumin)
from lvmcam.flir import ResetFLIR
from lvmcam.flir import FLIR_FullStatus

#from lvmieb.controller.controller import IebController
#from lvmieb.exceptions import LvmIebError

from . import parser


__all__ = ["camstat.py"]


@parser.group()
def camstat(*args):
    """control status of FLIR camera"""

    pass

@camstat.command()
#@click.option(
#   "-s",
#   "--side",
#   type=click.Choice(["all", "right", "left"]),
#   default = "all",
#   help="all, right, or left",
#)
async def readstat(command: Command):
    read_FLIR.readflir()
    command.info("test image and status of FLIR camera")

async def reset(command: Command):
    ResetFLIR.resetcam()
    command.info("FLIR reset")

async def fullstat(command: Command):
    FLIR_FullStatus.fullstat()
    command.info("full status of FLIR camera")



