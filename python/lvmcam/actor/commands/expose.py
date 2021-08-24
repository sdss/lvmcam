# @Author: Mingyu Jeon (mgjeon@khu.ac.kr)
# @Date: 2021-08-23
# @Filename: expose.py

from __future__ import absolute_import, annotations, division, print_function
import click
from click.decorators import command
from clu.command import Command
from . import parser

# exposure function
import asyncio
import os
from araviscam.araviscam import BlackflyCam as blc
from basecam.exposure import ImageNamer
image_namer = ImageNamer(
    "{camera.name}-{num:04d}.fits",
    dirname=".",
    overwrite=False,
)
async def exposure(exptime, name, num, filepath, config):
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    uid = cs._config['sci.agw']['uid']
    filepath = os.path.abspath(filepath)
    cam = await cs.add_camera(name=name, uid=uid)
    paths = []
    for i in range(num):
        filename = f'{name}-{image_namer(cam)}'
        paths.append(os.path.join(filepath, filename))
    for i in range(num):
        try:
            await cam.expose(exptime=exptime, filename=paths[i], write=True)
        except OSError:
            await cs.remove_camera(name=name, uid=uid)
            return "OSError"
    await cs.remove_camera(name=name, uid=uid)
    return paths

# actor
__all__ = ["expose"]

@parser.group()
def expose(*args):
    """[TEST] expose function of araviscam module."""
    pass

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
    paths = []

    try:
        paths = await exposure(
            exptime=exptime,
            name=name,
            num=num,
            filepath=filepath,
            config=config,
        )
    except OSError:
        command.error(path="OSError", info="File alreday exists.")
        return

    if (paths != "OSError"):
        command.finish(path=paths)
        return
    else:
        command.error(path="OSError", info="File alreday exists.")
        return
