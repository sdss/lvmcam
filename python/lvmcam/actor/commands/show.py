from __future__ import absolute_import, annotations, division, print_function

import asyncio
import os

import click
from click.decorators import command
from clu.command import Command

from lvmcam.actor import modules
from basecam.actor.commands import camera_parser as parser
# from lvmcam.actor.commands.connection import cam_list
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
@click.option("-v", "--verbose", is_flag=True)
async def all(command: Command, config: str, verbose: bool):
    """
    Show all cameras in configuration file.

    Parameter
    ----------
    config
        Name of the YAML file with the cameras configuration
    verbose
        Verbosity on or off
    """
    modules.change_dir_for_normal_actor_start(__file__)

    if verbose:
        modules.logger.sh.setLevel(int(verbose))
    else:
        modules.logger.sh.setLevel(modules.logging.WARNING)

    from lvmcam.araviscam import BlackflyCameraSystem, BlackflyCamera
    from lvmcam.skymakerca import SkyCameraSystem, SkyCamera

    camera_types = {"araviscam": (BlackflyCameraSystem, BlackflyCamera),
                    "skymakercam": (SkyCameraSystem, SkyCamera)}
    CameraSystem = camera_types[modules.variables.camtypename][0]
    Camera = camera_types[modules.variables.camtypename][1]

    cs, available_cameras_uid = find_all_available_cameras_for_show(config, CameraSystem, Camera, verbose)

    cameras_dict = {}
    for item in list(cs._config.items()):
        uid = item[1]["uid"]
        if uid in available_cameras_uid:
            cameras_dict[item[0]] = f"Available | uid: {uid}"
        else:
            cameras_dict[item[0]] = f"Unavailable | uid: {uid}"
    # command.info(ALL=cameras_dict)
    return command.finish(ALL=cameras_dict)


@modules.timeit
def find_all_available_cameras_for_show(config, CameraSystem, Camera, verbose):
    config = os.path.abspath(config)
    cs = CameraSystem(Camera, camera_config=config, verbose=verbose)
    available_cameras_uid = cs.list_available_cameras()
    return cs, available_cameras_uid


@show.command()
# @click.option("-c", "--config", type=str, default="python/lvmcam/etc/cameras.yaml")
async def connection(
    command: Command,
    # config: str,
):
    """
    Show all connected cameras.
    """
    modules.change_dir_for_normal_actor_start(__file__)
    # cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    cameras_dict = {}
    if modules.variables.cam_list:
        for i, cam in enumerate(modules.variables.cam_list):
            cameras_dict[i] = {"name": cam.name, "uid": cam.uid}
            # command.info(CONNECTED={"name": cam.name, "uid": cam.uid})
        return command.finish(CONNECTED=cameras_dict)
    else:
        command.error("There are no connected cameras")
        return command.fail()
