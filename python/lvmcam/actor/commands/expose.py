from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from araviscam.araviscam import BlackflyCamera as blc
from araviscam.araviscam import BlackflyCameraSystem as blcs
from basecam import (BaseCamera, CameraConnectionError, CameraEvent,
                     CameraSystem, Exposure, events, models,ImageNamer)
from clu.command import Command

# from lvmieb.controller.controller import IebController
from lvmcam.exceptions import LvmcamError

from . import parser

__all__ = ["expose"]


@parser.group()
def expose(*args):
    """expose function of araviscam module. internal returns buffer file
    and external returns fits file"""
    print(args)


@expose.command()
@click.argument("EXPT", type=float)
async def expsingle(command: Command, expt: float):

    try:
        print("before : ", blc)  # BlackflyCamera
        await blc._connect_internal(self=blc)
        print("after : ", blc)

        # print(blc.device)
        expflir = Exposure(blc)
        expflir.exptime = expt
        print(expflir)
        print(expflir.exptime)
        await blc._expose_grabFrame(self=blc, exposure=expflir)
        command.info("FLIR exposing...")
        print(expflir.data)

        await blc._disconnect_internal(self=blc)

    except LvmcamError as err:
        command.fail(f"error is {err}")
        # return command.finish()


@expose.command()
@click.argument("EXPTIME", type=float)
async def expfits(command: Command, expt: float):
    # try:
    #     # connect independently
    #     await blc._connect_internal(self=blc)

    #     # check connection
    #     # command.info(str(blc.device))
    #     expflir = Exposure(blc)
    #     expflir.exptime = expt

    #     # exopse
    #     reg = await blc.expose(exposure=expflir)
    #     command.info("FLIR exposing FITS...")
    #     path = ImageNamer
    #     await reg.write(path)

    #     # disconnect independently
    #     await blc._disconnect_internal(self=blc)

    # except LvmcamError as err:
    #     command.fail(f"error is {err}")

    # return command.finish(path=str(path))
    pass

# expose and make fits image and return path of fits image. (09/08/21 SML)


@expose.command()
@click.argument("EXPT", type=float)
async def exptest(command: Command, expt: float):
    cs = blcs(blc)
    cam = await cs.add_camera(uid="19283193")
    # print("cameras", cs.cameras)
    # print("config" ,config)
    exp = await cam.expose(expt, "LAB TEST")
    print(exp.data)
    command.info("FLIR exposing...")
    # return command.finish()
