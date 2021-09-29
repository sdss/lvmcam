from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from clu.command import Command

from lvmcam.flir.FLIR_Utils import Setup_Camera, custom_status

from . import parser


__all__ = ["status"]



@parser.command()
@click.option("-v", '--verbose', type=bool, default=False)
async def status(command: Command, verbose):
    """
    Show status of camera
    """
    try:
        cam, dev = Setup_Camera(verbose)
        command.info(status=await custom_status(cam, dev))
    except ValueError:
        command.error(error="There are not real cameras")    
    return
