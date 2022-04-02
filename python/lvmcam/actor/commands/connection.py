from __future__ import absolute_import, annotations, division, print_function

import asyncio
import collections
import datetime
from logging import raiseExceptions
import os

import click
import gi
from click.decorators import command
from clu.command import Command

from lvmcam.actor import modules
from basecam.actor.commands import camera_parser as parser
from lvmcam.flir import FLIR_Utils as flir
from sdsstools import read_yaml_file


__all__ = ["connect", "disconnect"]


@parser.command()
@click.option("-v", "--verbose", is_flag=True)
# Name of an optional YAML file
@click.option("-c", "--config", type=str, default="python/lvmcam/etc/cameras.yaml")
@click.option("-n", "--name", type=str, default="all")
async def connect(
    command: Command,
    verbose: bool,
    config: str,
    name: str,
):
    """
    Connect all available cameras

    Parameters
    ----------
    verbose
        Verbosity on or off
    config
        Name of the YAML file with the cameras configuration
    name
        Name of camera to connect
    """
    modules.change_dir_for_normal_actor_start(__file__)

    if verbose:
        modules.logger.sh.setLevel(int(verbose))
    else:
        modules.logger.sh.setLevel(modules.logging.WARNING)

    if (modules.variables.cs is not None) or (modules.variables.cam_list != []):
        command.error("Cameras are already connected")
        return command.fail()

    modules.variables.config = read_yaml_file(config)

    from lvmcam.araviscam import BlackflyCameraSystem, BlackflyCamera
    from lvmcam.skymakerca import SkyCameraSystem, SkyCamera

    camera_types = {"araviscam": (BlackflyCameraSystem, BlackflyCamera),
                    "skymakercam": (SkyCameraSystem, SkyCamera)}
    CameraSystem = camera_types[modules.variables.camtypename][0]
    Camera = camera_types[modules.variables.camtypename][1]

    # modules.variables.cam_list.append(await modules.variables.cs.add_camera(uid=modules.variables.cs._config[camname]["uid"]))
    available_cameras_uid = []

    available_cameras_uid = find_all_available_cameras(config, CameraSystem, Camera, verbose)

    if available_cameras_uid == []:
        modules.variables.cs = None
        modules.variables.cam_list.clear()
        command.error("There are not real cameras to connect")
        return command.fail()

    try:
        config_file = list(modules.variables.cs._config.items())

        if name == 'all':
            for camera_name, props in config_file:
                if props["uid"] in available_cameras_uid:
                    await connect_available_camera(props)
            raise Exception

        target_props = None
        is_name_in = False
        for camera_name, props in config_file:
            if camera_name == name:
                is_name_in = True
                target_props = props
                break

        if is_name_in is True:
            await connect_available_camera(target_props)
        else:
            modules.variables.cs = None
            modules.variables.cam_list.clear()
            command.error("There is no camera to match the given name")
            return command.fail()
    except gi.repository.GLib.GError as e:
        command.error(f"{e}")
        return command.fail()
    except Exception:
        pass

    flir.setup_camera()
    _dict = {}
    # print(modules.variables.Aravis_available_camera)
    if modules.variables.cam_list:
        for cam in modules.variables.cam_list:
            command.info(CAMERA={"name": cam.name, "uid": cam.uid})
            modules.variables.camdict[cam.name] = cam
            for key, (_, _, uid) in modules.variables.Aravis_available_camera.items():
                if cam.uid == uid:
                    _dict[cam.name] = modules.variables.Aravis_available_camera[key]
    modules.variables.Aravis_available_camera = _dict
    # print(modules.variables.Aravis_available_camera)
    return command.finish()


@modules.atimeit
async def connect_available_camera(props):
    modules.variables.cam_list.append(await modules.variables.cs.add_camera(uid=props["uid"]))


# @modules.timeit
# def get_cam_dev_for_header(item):
#     while True:
#         camera, device = flir.setup_camera()
#         if camera.get_device_id() == item[1]["uid"]:
#             modules.variables.dev_list[item[1]["name"]] = (camera, device)
#             break


@modules.timeit
def find_all_available_cameras(config, CameraSystem, Camera, verbose):
    config = os.path.abspath(config)
    modules.variables.cs = CameraSystem(Camera, camera_config=config, verbose=verbose)
    modules.variables.cs_list.append(modules.variables.cs)
    available_cameras_uid = modules.variables.cs.list_available_cameras()
    return available_cameras_uid


@parser.command()
async def disconnect(
    command: Command,
):
    """
    Disconnect all cameras
    """
    modules.change_dir_for_normal_actor_start(__file__)

    if modules.variables.cam_list:
        for cam in modules.variables.cam_list:
            try:
                await modules.variables.cs.remove_camera(uid=cam.uid)
            except AttributeError:
                pass
        modules.variables.cs = None
        modules.variables.cs_list.clear()
        modules.variables.cam_list.clear()
        modules.variables.camdict.clear()
        command.info("Cameras have been removed")
        return command.finish()
    else:
        command.error("There is nothing to remove")
        return command.fail()
