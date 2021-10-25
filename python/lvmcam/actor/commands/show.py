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

    Example
    -------

    .. code-block:: console

    $ clu
    lvmcam show all
    12:22:02.371 lvmcam >
    12:22:04.706 lvmcam i {
        "ALL": {
            "sci.agw": "Available",
            "sci.age": "Unavailable",
            "sci.agc": "Unavailable",
            "skyw.agw": "Unavailable",
            "skyw.age": "Unavailable",
            "skyw.agc": "Unavailable",
            "skye.agw": "Unavailable",
            "skye.age": "Unavailable",
            "skye.agc": "Unavailable",
            "spec.agw": "Unavailable",
            "spec.age": "Unavailable",
            "spec.agc": "Unavailable"
        }
    }
    12:22:04.711 lvmcam :
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

    Example
    -------

    .. code-block:: console

    $ clu
    lvmcam show connection
    12:22:57.797 lvmcam >
    12:22:57.853 lvmcam e {
        "text": "There are no connected cameras"
    }
    lvmcam connect
    12:23:01.094 lvmcam >
    12:23:06.110 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    12:23:06.119 lvmcam :
    lvmcam show connection
    12:23:09.535 lvmcam >
    12:23:09.592 lvmcam i {
        "CONNECTED": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    12:23:09.593 lvmcam :
    lvmcam disconnect
    12:23:13.638 lvmcam >
    12:23:13.999 lvmcam i {
        "text": "Cameras have been removed"
    }
    12:23:14.004 lvmcam :
    lvmcam show connection
    12:23:17.098 lvmcam >
    12:23:17.155 lvmcam e {
        "text": "There are no connected cameras"
    }
    """
    modules.change_dir_for_normal_actor_start(__file__)
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    if cams:
        for cam in cams:
            command.info(CONNECTED={"name": cam.name, "uid": cam.uid})
        return command.finish()
    else:
        return command.error("There are no connected cameras")
