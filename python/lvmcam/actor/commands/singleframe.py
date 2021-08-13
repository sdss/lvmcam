# @Author: Mingyu Jeon (mgjeon@khu.ac.kr)
# @Date: 2021-08-13
# @Filename: singleframe.py

from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from araviscam.araviscam import BlackflyCam as blc
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


async def singleFrame(config, verbose, name, exptime, filepath):
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config, verbose=verbose)
    cam = await cs.add_camera(name=name, uid=cs._config['sci.agw']['uid'])
    exp = await cam.expose(exptime, "LAB TEST")
    await cs.remove_camera(name=name, uid=cs._config['sci.agw']['uid'])
    filepath = os.path.join(filepath, exp.filename)
    await exp.write(filename=filepath)
    return filepath


@singleframe.command()
# @click.option(
#   "-s",
#   "--side",
#   type=click.Choice(["all", "right", "left"]),
#   default = "all",
#   help="all, right, or left",
# )
@click.argument("EXPTIME", type=float, default=0.5)  # capital letter
@click.argument("FILEPATH", type=str,
                default="/home/mgjeon/lvmcam/python/lvmcam/assets")  # capital letter
@click.option('--verbose', type=bool, default=False)
@click.option('--name', type=str, default="test")
@click.option('--config', type=str, default="/home/mgjeon/lvmcam/python/lvmcam/etc/cameras.yaml")
async def singleexpose(
    command: Command,
    exptime: float,
    filepath: str,
    verbose: bool,
    name: str,
    config: str
):
    filepath = await singleFrame(
        config=config,
        verbose=verbose,
        name=name,
        exptime=exptime,
        filepath=filepath
    )
    command.info(f"Created {filepath}")
