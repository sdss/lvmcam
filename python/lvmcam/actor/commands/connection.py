from __future__ import absolute_import, annotations, division, print_function

import asyncio
import datetime
import os

import click
import gi
from click.decorators import command
from clu.command import Command

from lvmcam.actor.commands import parser
from lvmcam.araviscam import BlackflyCam as blc
import collections


__all__ = ["connect", "disconnect"]
cs = ""
csa = []
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


def pretty(time):
    return f"{bcolors.OKCYAN}{bcolors.BOLD}{time}{bcolors.ENDC}"


def pretty2(time):
    return f"{bcolors.OKGREEN}{bcolors.BOLD}{time}{bcolors.ENDC}"


@parser.command()
@click.option("-t", '--test', is_flag=True, help="Connect virtual camera for test")

@click.option("-v", '--verbose', is_flag=True)

# Name of an optional YAML file
@click.option("-c", '--config', type=str, default="python/lvmcam/etc/cameras.yaml", help="YAML file of lvmt cameras")

# With the -i switch we can add an explicit IP-Adress for a
# camera if we want to read a camera that is not reachable
# by the broadcast scanner.
# @click.option("-i", '--ip', help="IP address of camera")
async def connect(
    command: Command,
    test: bool,
    verbose: bool,
    config: str,
):
    """
    Connect all available cameras
    """
    os.chdir(os.path.dirname(__file__))
    os.chdir('../')
    os.chdir('../')
    os.chdir('../')
    os.chdir('../')
    global cs
    global csa
    global cams
    global camdict
    if(cs != ""):
        command.error(error="Cameras are already connected")
        return
    if(test):
        testcamdict = {"name":"test", "uid":"-1"}
        testcam = collections.namedtuple("ObjectName", testcamdict.keys())(*testcamdict.values())
        cams.append(testcam)
    else:

        if verbose : print(f"{datetime.datetime.now()} |lvmcam/connection.py| Find all available cameras")

        config = os.path.abspath(config)
        # print(config)
        cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
        csa.append(cs)
        available_cameras_uid = cs.list_available_cameras()
        if (available_cameras_uid == []):
            command.error(error="There are not real cameras to connect")
            return
        try:
            for item in list(cs._config.items()):
                if item[1]['uid'] in available_cameras_uid:

                    if verbose : print(f"{pretty(datetime.datetime.now())} |lvmcam/connection.py| Connecting {item[1]['name']} ...")

                    cams.append(await cs.add_camera(uid=item[1]['uid']))

                    if verbose : print(f"{pretty2(datetime.datetime.now())} |lvmcam/connection.py| Connected {item[1]['name']} ...")

        except gi.repository.GLib.GError:
            command.error(error="Cameras are already connected")
            return 

    if cams:
        for cam in cams:
            command.info(connect={"name": cam.name, "uid": cam.uid})
            camdict[cam.name] = cam
            # print(camdict)
    return command.finish(text="done")


@parser.command()
async def disconnect(
    command: Command,
):
    """
    Disconnect all cameras
    """
    os.chdir(os.path.dirname(__file__))
    os.chdir('../')
    os.chdir('../')
    os.chdir('../')
    os.chdir('../')
    global cs
    global cams
    if cams:
        for cam in cams:
            try:
                if (cam.name != "test"):
                    await cs.remove_camera(uid=cam.uid)
            except AttributeError:
                pass
        cs = ""
        csa.clear()
        cams.clear()
        camdict.clear()
        command.info("Cameras have been removed")
        return
    else:
        command.error(error="There is nothing to remove")
        return
