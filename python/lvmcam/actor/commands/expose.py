# @Author: Mingyu Jeon (mgjeon@khu.ac.kr)
# @Date: 2021-08-23
# @Filename: expose.py

from __future__ import absolute_import, annotations, division, print_function

import asyncio
import datetime
import functools
import os

import click
from click.decorators import command
from clu.command import Command

import lvmcam.actor.commands.camstatus as camstatus
from lvmcam.actor.commands import parser
from lvmcam.actor.commands.connection import camdict
from lvmcam.araviscam import BlackflyCam as blc


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


__all__ = ["expose"]



import basecam

from basecam.exposure import ImageNamer
image_namer = ImageNamer(
    "{camera.name}-{num:08d}.fits",
    dirname=".",
    overwrite=False,
)


@parser.command()
@click.argument("EXPTIME", type=float)
@click.argument('NUM', type=int)
@click.argument('CAMNAME', type=str)
@click.argument("FILEPATH", type=str, default="python/lvmcam/assets")
async def expose(
    command: Command,
    exptime: float,
    num: int,
    camname: str,
    filepath: str,
):
    """
    Do 'EXPTIME' expose 'NUM' times by using 'CAMNAME' camera.
    """
    print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | expose function start")
    if(not camdict):
        command.error(error="There are no connected cameras")
        return
    cam = camdict[camname]
    camera, device = camstatus.Setup_Camera(True)
    exps = []
    hdrs = []
    status = []
    for i in range(num):
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Expose start")
        exps.append(await cam.expose(exptime=exptime, image_type="object"))
        status.append(await camstatus.custom_status(camera, device))
        hdrs.append(cam.header)
        # hdr = exp[0].
        # hdrs.append(hdr)
        # await cam.expose(exptime=exptime, filename=paths[i], write=True)
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Expose done")

    # print(status)
    hdus = []
    dates = []
    for i in range(num):
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Setting header start")
        hdu = exps[i].to_hdu()[0]
        dates.append(hdu.header['DATE-OBS'])
        for item in hdrs[i]:
            hdr = item[0]
            val = item[1]
            com = item[2]
            hdu.header[hdr] = (val, com)
        for item in list(status[i].items()):
            hdr = item[0]
            val = item[1]
            if len(val) > 70:
                continue
            _hdr = hdr.replace(" ", "")
            _hdr = _hdr.replace(".", "")
            _hdr = _hdr.upper()[:8]
            hdu.header[_hdr] = (val, hdr)

        hdus.append(hdu)
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Setting header done")

    # for hdu in hdus: print(repr(hdu.header))

    print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Making filename start")
    filepath = os.path.abspath(filepath)
    paths = []
    for i in range(num):
        filename = image_namer(cam)
        print(filename)
        paths.append(os.path.join(filepath, filename))
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Ready for {paths[i]}")
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Write start")
        writeto_partial = functools.partial(
            hdus[i].writeto, paths[i], checksum=True
        )
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, writeto_partial)
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Write done")
    print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Making filename done")
    command.finish(path=paths)
    print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | expose function done")
    return
