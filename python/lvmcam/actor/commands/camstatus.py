from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from clu.command import Command

from lvmcam.flir import FLIR_Utils as flir

from basecam.actor.commands import camera_parser as parser

from lvmcam.actor import modules


__all__ = ["status"]


@parser.command()
async def status(command: Command):
    """
    Show status of camera
    """
    try:
        flir.setup_camera()
        if modules.variables.Aravis_available_camera == {}:
            raise ValueError
        for cam, dev, uid in modules.variables.Aravis_available_camera.values():
            status = await get_status_from_cam_dev(cam, dev)
            command.info(UID=uid)
            command.info(STATUS=status)
        command.finish()
    except ValueError:
        command.error("There are not real cameras")
        command.fail()
    return


@modules.atimeit
async def get_status_from_cam_dev(cam, dev):
    status = await flir.custom_status(cam, dev)
    return status
