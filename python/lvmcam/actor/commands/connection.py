from __future__ import absolute_import, annotations, division, print_function
import click
from click.decorators import command
from clu.command import Command
from lvmcam.actor.commands import parser

import asyncio
import os
from araviscam.araviscam import BlackflyCam as blc

import gi

__all__ = ["connect", "disconnect"]

cs = ""
cams = []
camdict = {}

@parser.command()
@click.argument('CONFIG', type=str, default="python/lvmcam/etc/cameras.yaml")
async def connect(
    command: Command,
    config: str,
):
    global cs
    config = os.path.abspath(config)
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    available_cameras_uid = cs.list_available_cameras()
    global cams
    global camdict
    try:
        for item in list(cs._config.items()):
            if item[1]['uid'] in available_cameras_uid:
                cams.append(await cs.add_camera(uid=item[1]['uid']))
    except gi.repository.GLib.GError:
        command.error(error="Already camera is connected")
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
