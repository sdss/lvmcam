from __future__ import absolute_import, annotations, division, print_function

import asyncio
import os

import click
from click.decorators import command
from clu.command import Command

from lvmcam.actor import modules
from lvmcam.actor.commands import parser
from lvmcam.actor.commands.connection import cams
from lvmcam.araviscam import BlackflyCam as blc


__all__ = ["show"]


@parser.group()
def show(*args):
    """
    all / connection
    """
    pass


@show.command()
@click.option(
    "-c",
    "--config",
    type=str,
    default="python/lvmcam/etc/cameras.yaml",
    help="YAML file of lvmt cameras",
)
async def all(
    command: Command,
    config: str,
):
    """
    Show all cameras in configuration file.
    """
    modules.change_dir_for_normal_actor_start(__file__)
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    available_cameras_uid = cs.list_available_cameras()
    for item in list(cs._config.items()):
        if item[1]["uid"] in available_cameras_uid:
            command.write("i", f"available: {item}")
        else:
            command.write("i", f"unavailable: {item}")
    return command.finish()


@show.command()
@click.option(
    "-c",
    "--config",
    type=str,
    default="python/lvmcam/etc/cameras.yaml",
    help="YAML file of lvmt cameras",
)
async def connection(
    command: Command,
    config: str,
):
    """
    Show all connected cameras.
    """
    modules.change_dir_for_normal_actor_start(__file__)
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    if cams:
        for cam in cams:
            command.write("i", f"{{ 'name': {cam.name}, 'uid': {cam.uid} }}")
        return command.finish()
    else:
        return command.error("There are no connected cameras")
