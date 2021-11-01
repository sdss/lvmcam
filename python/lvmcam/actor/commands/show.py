from __future__ import absolute_import, annotations, division, print_function

import asyncio
import os

import click
from click.decorators import command
from clu.command import Command

from lvmcam.actor import modules
from lvmcam.actor.commands import parser
from lvmcam.actor.commands.connection import cam_list
from lvmcam.araviscam import BlackflyCam as blc
from lvmcam.araviscam.aravis import Aravis


__all__ = ["show"]


@parser.group()
def show(*args):
    """
    all / connection
    """
    pass


@show.command()
@click.option("-c", "--config", type=str, default="python/lvmcam/etc/cameras.yaml")
async def all(
    command: Command,
    config: str,
):
    """
    Show all cameras in configuration file.

    Parameter
    ----------
    config
        Name of the YAML file with the cameras configuration
    """
    modules.change_dir_for_normal_actor_start(__file__)
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    available_cameras_uid = cs.list_available_cameras()
    cameras_dict = {}
    for item in list(cs._config.items()):
        if item[1]["uid"] in available_cameras_uid:
            cameras_dict[item[0]] = "Available"
        else:
            cameras_dict[item[0]] = "Unavailable"
    command.info(ALL=cameras_dict)
    return command.finish()


@show.command()
@click.option("-c", "--config", type=str, default="python/lvmcam/etc/cameras.yaml")
async def connection(
    command: Command,
    config: str,
):
    """
    Show all connected cameras.

    Parameter
    ----------
    config
        Name of the YAML file with the cameras configuration
    """
    modules.change_dir_for_normal_actor_start(__file__)
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    if cam_list:
        for cam in cam_list:
            command.info(CONNECTED={"name": cam.name, "uid": cam.uid})
        return command.finish()
    else:
        return command.error("There are no connected cameras")
