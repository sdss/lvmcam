from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from araviscam.araviscam import BlackflyCamera as blc
from araviscam.araviscam import BlackflyCameraSystem as blcs
from clu.command import Command

from . import parser


# from lvmieb.controller.controller import IebController
# from lvmieb.exceptions import LvmIebError


__all__ = ["connect"]


@parser.group()
def connect(*args):
    """connection via BlackflyCameraSystem Class. Changing .Yaml file of
    aravicam module is neeeded when changing the camera"""

    pass


@connect.command()
# @click.option(
#   "-s",
#   "--side",
#   type=click.Choice(["all", "right", "left"]),
#   default = "all",
#   help="all, right, or left",
# )
async def listcams(command: Command):
  command.info(str(blcs.list_available_cameras(self=blcs)))
  command.info("Available cameras")

@connect.command()
async def con(command: Command):
    await blc._connect_internal(self=blc)
    command.info("FLIR connecting")


@connect.command()
async def discon(command: Command):
    await blc._disconnect_internal(self=blc)
    command.info("FLIR disconnecting")