# @Author: Mingyu Jeon (mgjeon@khu.ac.kr)
# @Date: 2021-08-23
# @Filename: expose.py

from __future__ import absolute_import, annotations, division, print_function
import click
from click.decorators import command
from clu.command import Command
from . import parser

# actor
__all__ = ["expose"]

@parser.group()
def expose(*args):
    """[TEST] expose function of araviscam module."""
    pass

import asyncio
import os
from araviscam.araviscam import BlackflyCam as blc
from basecam.exposure import ImageNamer
image_namer = ImageNamer(
    "{camera.name}-{num:04d}.fits",
    dirname=".",
    overwrite=False,
)
@expose.command()
@click.argument("EXPTIME", type=float)
@click.argument('NAME', type=str)
@click.argument('NUM', type=int)
@click.argument("FILEPATH", type=str, default="python/lvmcam/assets")
@click.argument('CONFIG', type=str, default="python/lvmcam/etc/cameras.yaml")
async def start(
    command: Command,
    exptime: float,
    name: str,
    num: int,
    filepath: str,
    config: str,
):

    command.info("Actor started")

    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    uid = cs._config['sci.agw']['uid']
    cam = await cs.add_camera(name=name, uid=uid)
    command.info("Camera Added")

    command.info("Start making filenames")
    paths = []
    filepath = os.path.abspath(filepath)
    for i in range(num):
        filename = f'{name}-{image_namer(cam)}'
        paths.append(os.path.join(filepath, filename))
        command.info(f"Ready for {paths[i]}")
    for i in range(num):
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Exposure Start")
        try:
            await cam.expose(exptime=exptime, filename=paths[i], write=True)
        except OSError:
            await cs.remove_camera(name=name, uid=uid)
            command.error(path="OSError", info="File alreday exists.")
            return
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Exposure Stop")
    await cs.remove_camera(name=name, uid=uid)
    command.finish(path=paths)

cs = ""
cam = ""

@expose.command()
@click.argument('NAME', type=str)
@click.argument('CONFIG', type=str, default="python/lvmcam/etc/cameras.yaml")
async def addcam(
    command: Command,
    name: str,
    config: str,
):
    global cs
    global cam
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    uid = cs._config['sci.agw']['uid']
    cam = await cs.add_camera(name=name, uid=uid)
    command.info("Camera Added")
    return
    
@expose.command()
async def showcam(
    command: Command,
):
    global cam
    if(cam):
        command.info(f"Connected: {cam.uid}")
        return
    else:
        command.error("Nothing connected")
        return


@expose.command()
@click.argument("EXPTIME", type=float)
@click.argument('PREFIX', type=str)
@click.argument('NUM', type=int)
@click.argument("FILEPATH", type=str, default="python/lvmcam/assets")
async def main(
    command: Command,
    exptime: float,
    prefix: str,
    num: int,
    filepath: str,
):
    global cs
    global cam
    if(not cam):
        command.error("Camera doesn't exist")
        return
    exps = []
    for i in range(num):
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Exposure Start")
        exps.append(await cam.expose(exptime=exptime))
        # await cam.expose(exptime=exptime, filename=paths[i], write=True)
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Exposure Done")
    
    command.info("Start making filenames")
    filepath = os.path.abspath(filepath)
    paths = []
    for i in range(num):
        filename = f'{prefix}-{image_namer(cam)}'
        paths.append(os.path.join(filepath, filename))
        command.info(f"Ready for {paths[i]}")
    hdus = []
    for i in range(num):
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Save Start")
        hdus.append(exps[i].to_hdu())
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Save Done")
    print(hdus)
    # await cs.remove_camera(uid=cam.name)
    command.finish(path=paths)
    return

@expose.command()
async def removecam(
    command: Command,
):
    if(cam):
        await cs.remove_camera(uid=cam.name)
        command.finish("Camera hvae been removed")
        return
    else:
        command.error("Nothing to remove")
        return