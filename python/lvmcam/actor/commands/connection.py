from __future__ import absolute_import, annotations, division, print_function
import click
from click.decorators import command
from clu.command import Command
from lvmcam.actor.commands import parser

import asyncio
import os
from lvmcam.araviscam import BlackflyCam as blc

import gi

__all__ = ["connect", "disconnect"]

cs = ""
cams = []
camdict = {}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import datetime

def pretty(time):
    return f"{bcolors.OKCYAN}{bcolors.BOLD}{time}{bcolors.ENDC}"


@parser.command()
@click.argument('CONFIG', type=str, default="python/lvmcam/etc/cameras.yaml")
async def connect(
    command: Command,
    config: str,
):
    """
    Connect all available cameras
    """
    global cs
    config = os.path.abspath(config)
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    available_cameras_uid = cs.list_available_cameras()
    print(f"{pretty(datetime.datetime.now())} Find all available cameras")
    global cams
    global camdict
    try:
        for item in list(cs._config.items()):
            if item[1]['uid'] in available_cameras_uid:
                print(f"{pretty(datetime.datetime.now())} Connecting {item[1]['name']} ...")
                cams.append(await cs.add_camera(uid=item[1]['uid']))
                print(f"{pretty(datetime.datetime.now())} Connected {item[1]['name']} ...")
    except gi.repository.GLib.GError:
        command.error(error="Cameras are already connected")
        return

    if cams:
        for cam in cams:
            command.info(connect={"name":cam.name, "uid":cam.uid})
        for cam in cams:
            camdict[cam.name]=cam
            # print(camdict)
    return

@parser.command()
async def disconnect(
    command: Command,
):
    """
    Disconnect all cameras
    """
    global cs
    global cams
    if cams:
        for cam in cams:
            await cs.remove_camera(uid=cam.uid)
            command.info("Camera have been removed")
        cams.clear()
        camdict.clear()
        return
    else:
        command.error(error="There is nothing to remove")
        return