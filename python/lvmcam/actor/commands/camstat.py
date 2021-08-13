from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from clu.command import Command

from lvmcam.flir import (read_FLIR)  # auto run when actor started (30/07/21 Sumin)
from lvmcam.flir import FLIR_FullStatus, ResetFLIR, FLIR_Utils

from . import parser


#from lvmieb.controller.controller import IebController
#from lvmieb.exceptions import LvmIebError

__all__ = ["camstat"]


# currently not working due to problem of flir_utils
@parser.group()
def camstat(*args):
    """control status of FLIR camera"""
    print(args)


@camstat.command()
# @click.option(
#    "-s",
#    "--side",
#    type=click.Choice(["all", "right", "left"]),
#    default = "all",
#    help="all, right, or left",
# )
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


@camstat.command()
async def acquire(command: Command):
    camt, devt = FLIR_Utils.Setup_Camera(False)
    command.info(str(FLIR_Utils.Acquire_Frames(cam=camt, nFrames=1)))
    command.info("exposing single frame for test")
