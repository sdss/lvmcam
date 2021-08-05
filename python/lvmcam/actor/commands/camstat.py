from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from clu.command import Command

from lvmcam.flir import (read_FLIR)  # auto run when actor started (30/07/21 Sumin)
from lvmcam.flir import FLIR_FullStatus, ResetFLIR

from . import parser


#from lvmieb.controller.controller import IebController
#from lvmieb.exceptions import LvmIebError



__all__ = ["camstat"]


@parser.group()
def camstat(*args):
    """control status of FLIR camera"""
#currently not working due to problem of flir_utils
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

@camstat.command()
async def reset(command: Command):
    ResetFLIR.resetcam()
    command.info("FLIR reset")

@camstat.command()
async def fullstat(command: Command):
    FLIR_FullStatus.fullstat()
    command.info("full status of FLIR camera")



