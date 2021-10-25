from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from clu.command import Command

from lvmcam.flir import FLIR_Utils as flir

from . import parser


__all__ = ["status"]


@parser.command()
@click.option("-v", "--verbose", type=bool, default=False)
async def status(command: Command, verbose):
    """
    Show status of camera
    """
    try:
        cam, dev = flir.setup_camera(verbose)
        status = await flir.custom_status(cam, dev)
    except ValueError:
        command.error("There are not real cameras")

    command.info(STATUS=status)
    return command.finish()
