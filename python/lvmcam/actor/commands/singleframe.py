# @Author: Mingyu Jeon (mgjeon@khu.ac.kr)
# @Date: 2021-08-13
# @Filename: singleframe.py

from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from araviscam.araviscam import BlackflyCam as blc
from click.decorators import command
from clu.command import Command
import os

from . import parser


# from lvmieb.controller.controller import IebController
# from lvmieb.exceptions import LvmIebError


__all__ = ["singleframe"]


@parser.group()
def singleframe(*args):
    """singleframe expose. fixed expose time (0.5sec) returns fits file"""
    pass


async def singleFrame(config, name, exptime, filepath, overwrite, num):
    # cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config, verbose=verbose)
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    cam = await cs.add_camera(name=name, uid=cs._config['sci.agw']['uid'])
    filepaths = []
    for i in range(num):
        exp = await cam.expose(exptime)
        # await cs.remove_camera(name=name, uid=cs._config['sci.agw']['uid'])
        filepath = os.path.abspath(filepath)
        exp.filename = f'{name}_{exp.filename}'
        # if(name):
        #     exp.filename = name + ".fits"
        # filepath = os.path.join(filepath, exp.filename)
        filepaths.append(os.path.join(filepath, exp.filename))
        await exp.write(filename=filepaths[i], overwrite=overwrite)
    await cs.remove_camera(name=name, uid=cs._config['sci.agw']['uid'])
    return filepath


@singleframe.command()
# @click.option(
#   "-s",
#   "--side",
#   type=click.Choice(["all", "right", "left"]),
#   default = "all",
#   help="all, right, or left",
# )
@click.argument("EXPTIME", type=float)
# @click.option('--verbose', type=bool, default=False)
@click.argument('NAME', type=str)
@click.argument('NUM', type=int)
@click.argument("FILEPATH", type=str, default="python/lvmcam/assets")
@click.argument('CONFIG', type=str, default="python/lvmcam/etc/cameras.yaml")
@click.option('--overwrite', type=bool, default=False)
async def singleexpose(
    command: Command,
    exptime: float,
    name: str,
    num: int,
    filepath: str,
    # verbose: bool,
    config: str,
    overwrite: bool
):
    fitspath = ""

    try:
        fitspath = await singleFrame(
            exptime=exptime,
            name=name,
            num=num,
            filepath=filepath,
            config=config,
            # verbose=verbose,
            overwrite=overwrite
        )
    except OSError:
        command.info("File alreday exists. See traceback in the log for more information.")
        command.info("If you want to overwrite the file, set --overwrite True.")
        command.finish(path="OSError", info="File alreday exists. See traceback in the log for more information.")
        return

    if (fitspath):
        command.info(f"Created {fitspath}")
        command.finish(path=fitspath)
        return
    else:
        command.finish(path="File not written")
        return

