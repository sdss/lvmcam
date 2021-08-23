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
async def exposure(exptime, name, num, filepath, config, overwrite):
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    cam = await cs.add_camera(name=name, uid=cs._config['sci.agw']['uid'])
    filepath = os.path.abspath(filepath)
    exps = []
    paths = []
    for i in range(num):
        exp = await cam.expose(exptime=exptime)
        exp.filename = f'{name}_{exp.filename}'
        exps.append(exp)
        paths.append(os.path.join(filepath, exp.filename))
    for i in range(num):
        try:
            await exps[i].write(filename=paths[i], overwrite=overwrite)
        except OSError:
            await cs.remove_camera(name=name, uid=cs._config['sci.agw']['uid'])
            return "Error"
    await cs.remove_camera(name=name, uid=cs._config['sci.agw']['uid'])
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
@click.option('--overwrite', type=bool, default=False)
async def start(
    command: Command,
    exptime: float,
    name: str,
    num: int,
    filepath: str,
    config: str,
    overwrite: bool
):
    paths = []

    try:
        paths = await exposure(
            exptime=exptime,
            name=name,
            num=num,
            filepath=filepath,
            config=config,
            overwrite=overwrite
        )
    except OSError:
        command.info("File alreday exists. See traceback in the log for more information.")
        command.info("If you want to overwrite the file, set --overwrite True.")
        command.finish(path="OSError", info="File alreday exists. See traceback in the log for more information.")
        return

    if (paths != "Error"):
        command.finish(path=paths)
        return
    else:
        command.finish(path="File already exists")
        return
