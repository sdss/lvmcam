from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from clu.command import Command

from lvmcam.flir.FLIR_Utils import Setup_Camera, custom_status

from . import parser


__all__ = ["status"]


# def get_camera():
#     Aravis.update_device_list()
#     camera = Aravis.Camera.new(Aravis.get_device_id(0))
#     device = camera.get_device()
#     return camera, device


@parser.command()
@click.option('--verbose', type=bool, default=False)
async def status(command: Command, verbose):
    """
    Show status of camera
    """
    # print(Aravis.get_device_id(0))
    cam, dev = Setup_Camera(verbose)
    # cam,dev = FLIR_Utils.Setup_Camera(verbose,False)
    # FLIR_Utils.Standard_Settings(cam,dev,verbose)
    command.info(status=await custom_status(cam, dev))
    return
