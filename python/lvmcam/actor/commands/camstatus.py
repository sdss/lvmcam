from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from clu.command import Command

from lvmcam.flir import FLIR_Utils as flir

from basecam.actor.commands import camera_parser as parser

from lvmcam.actor import modules


__all__ = ["status"]


@parser.command()
@click.option("-v", "--verbose", is_flag=True)
async def status(command: Command, verbose):
    """
    Show status of camera

    Parameters
    ----------
    verbose
        Verbosity on or off
    """
    if verbose:
        modules.logger.sh.setLevel(int(verbose))
    else:
        modules.logger.sh.setLevel(modules.logging.WARNING)

    try:
        flir.setup_camera()
        for cam, dev, uid in modules.variables.Aravis_available_camera.values():
            status = await get_status_from_cam_dev(cam, dev)
            command.info(UID=uid)
            command.info(STATUS=status)
    except ValueError:
        command.error("There are not real cameras")

    return command.finish()


@modules.atimeit
async def get_status_from_cam_dev(cam, dev):
    status = await flir.custom_status(cam, dev)
    return status
