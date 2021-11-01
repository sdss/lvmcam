from __future__ import absolute_import, annotations, division, print_function

import asyncio
import collections
import datetime
import os

import click
import gi
from click.decorators import command
from clu.command import Command

from lvmcam.actor import modules
from lvmcam.actor.commands import parser
from lvmcam.araviscam import BlackflyCam as blc
from lvmcam.flir import FLIR_Utils as flir


__all__ = ["connect", "disconnect"]

cs = ""
cs_list = []
cam_list = []
dev_list = {}
camdict = {}


@parser.command()
@click.option("-t", "--test", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
# Name of an optional YAML file
@click.option("-c", "--config", type=str, default="python/lvmcam/etc/cameras.yaml")
# With the -i switch we can add an explicit IP-Adress for a
# camera if we want to read a camera that is not reachable
# by the broadcast scanner.
@click.option("-i", "--ip")
async def connect(
    command: Command,
    test: bool,
    verbose: bool,
    config: str,
    ip=None,
):
    """
    Connect all available cameras

    Parameters
    ----------
    test
        Connection to test camera on or off
    verbose
        Verbosity on or off
    config
        Name of the YAML file with the cameras configuration
    ip
        list of explicit IP's (like 192.168.70.51 or lvmt.irws2.mpia.de)
    """
    modules.change_dir_for_normal_actor_start(__file__)
    global cs
    global cs_list
    global cam_list
    global dev_list
    global camdict
    if cs != "" or cam_list != []:
        return command.error("Cameras are already connected")
    if test:
        test_camdict = {"name": "test", "uid": "-1"}
        test_cam = collections.namedtuple("ObjectName", test_camdict.keys())(
            *test_camdict.values()
        )
        cam_list.append(test_cam)
    else:

        if verbose:
            print(modules.current_progress(__file__, "Find all available cameras"))

        config = os.path.abspath(config)
        cs = blc.BlackflyCameraSystem(
            blc.BlackflyCamera, camera_config=config, verbose=verbose, ip_list=ip
        )
        cs_list.append(cs)
        available_cameras_uid = cs.list_available_cameras()
        if available_cameras_uid == []:
            return command.error("There are not real cameras to connect")
        try:
            for item in list(cs._config.items()):
                if item[1]["uid"] in available_cameras_uid:

                    if verbose:
                        print(
                            modules.current_progress(
                                __file__, f"Connecting {item[1]['name']} ..."
                            )
                        )

                    cam_list.append(await cs.add_camera(uid=item[1]["uid"]))
                    while True:
                        camera, device = flir.setup_camera(verbose)
                        if camera.get_device_id() == item[1]["uid"]:
                            dev_list[item[1]["name"]] = (camera, device)
                            break

                    if verbose:
                        print(
                            modules.current_progress(
                                __file__, f"Connected {item[1]['name']} ..."
                            )
                        )

        except gi.repository.GLib.GError:
            return command.error("Cameras are already connected")

    if cam_list:
        for cam in cam_list:
            command.info(CAMERA={"name": cam.name, "uid": cam.uid})
            camdict[cam.name] = cam
    return command.finish()


@parser.command()
async def disconnect(
    command: Command,
):
    """
    Disconnect all cameras
    """
    modules.change_dir_for_normal_actor_start(__file__)
    global cs
    global cs_list
    global cam_list
    global camdict
    if cam_list:
        for cam in cam_list:
            try:
                if cam.name != "test":
                    await cs.remove_camera(uid=cam.uid)
            except AttributeError:
                pass
        cs = ""
        cs_list.clear()
        cam_list.clear()
        camdict.clear()
        command.write("i", "Cameras have been removed")
        return command.finish()
    else:
        return command.error("There is nothing to remove")
