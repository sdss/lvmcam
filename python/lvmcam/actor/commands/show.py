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
from lvmcam.araviscam.aravis import Aravis


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
    """
    modules.change_dir_for_normal_actor_start(__file__)
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    if cams:
        for cam in cams:
            command.info(CONNECTED={"name": cam.name, "uid": cam.uid})
        return command.finish()
    else:
        return command.error("There are no connected cameras")


@show.command()
@click.option(
    "-c",
    "--config",
    type=str,
    default="python/lvmcam/etc/cameras.yaml",
    help="YAML file of lvmt cameras",
)
@click.argument("IPLIST", type=str)
async def ip(
    command: Command,
    config: str,
    iplist: str,
):
    """
    Show all available cameras based on ip-address
    """
    modules.change_dir_for_normal_actor_start(__file__)

    # Start with (pessimistic) initially empty set of online devices
    serialNums = []
    addrs = []

    # Aravis.update_device_list()
    # Ndev = Aravis.get_n_devices()
    # # print(str(Ndev) + " cameras online")

    # # get_device_id returns a string of type, SN, MAC etc
    # for i in range(Ndev):
    #     cam = Aravis.Camera.new(Aravis.get_device_id(i))
    #     uid = cam.get_string("DeviceSerialNumber")
    #     serialNums.append(uid)
    #     addrs.append("")

    # print(iplist)

    try:
        cam = Aravis.Camera.new(iplist)
        uid = cam.get_string("DeviceSerialNumber")
        # If is this was already in the scan: discard, else add
        if uid not in serialNums:
            serialNums.append(uid)
            addrs.append("@" + iplist)
    except:
        # apparently no such camera at this address....
        pass
    # for ip in self.ips_nonlocal:
    #     try:
    #         cam = Aravis.Camera.new(ip)
    #         uid = cam.get_string("DeviceSerialNumber")
    #         # If is this was already in the scan: discard, else add
    #         if uid not in serialNums:
    #             serialNums.append(uid)
    #             addrs.append("@" + ip)
    #     except:
    #         # apparently no such camera at this address....
    #         pass
    try:
        return command.finish(f"{uid}")
    except UnboundLocalError:
        return command.error("There is no camera matched with the ip address")
