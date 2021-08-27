from __future__ import absolute_import, annotations, division, print_function
import click
from click.decorators import command
from clu.command import Command
from lvmcam.actor.commands import parser

import asyncio
from araviscam.araviscam import BlackflyCam as blc

from lvmcam.actor.commands.connection import cams

__all__ = ["show"]

def show_available_camera(command, cs):
    available_cameras_uid = cs.list_available_cameras()
    for item in list(cs._config.items()):
        if item[1]['uid'] in available_cameras_uid:
            command.info(available=f"{item}")
        else:
            command.error(unavailable=f"{item}")
    return

def show_connected_camera(command, cs):
    if cams:
        for cam in cams:
            command.info(connect={"name":cam.name, "uid":cam.uid})
        return
    else:
        command.error(error="There are no connected cameras")
        return


@parser.group()
def show(*args):
    """
    all / connection
    """
    pass

@show.command()
@click.argument('CONFIG', type=str, default="python/lvmcam/etc/cameras.yaml")
async def all(
    command: Command,
    config: str,
):
    """
    Show all cameras in configuration file.
    """
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    show_available_camera(command, cs)
    return

@show.command()
@click.argument('CONFIG', type=str, default="python/lvmcam/etc/cameras.yaml")
async def connection(
    command: Command,
    config: str,
):
    """
    Show all connected cameras.
    """
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    show_connected_camera(command, cs)
    return


