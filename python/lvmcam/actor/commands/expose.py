# @Author: Mingyu Jeon (mgjeon@khu.ac.kr)
# @Date: 2021-08-23
# @Filename: expose.py

from __future__ import absolute_import, annotations, division, print_function
import click
from click.decorators import command
from clu.command import Command
from lvmcam.actor.commands import parser

from lvmcam.actor.commands.connection import camdict
import lvmcam.actor.commands.camstatus as camstatus

__all__ = ["expose"]

import asyncio
import os
from araviscam.araviscam import BlackflyCam as blc
# from basecam.exposure import ImageNamer
# image_namer = ImageNamer(
#     "{camera.name}-{num:04d}.fits",
#     dirname=".",
#     overwrite=False,
# )
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
    if(not camdict):
        command.error(error="There are no cameras connected")
        return
    cam = camdict[camname]
    camera, device = camstatus.get_camera()
    exps = []
    status = []
    for i in range(num):
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Expose Start")
        exps.append(await cam.expose(exptime=exptime))
        status.append(await camstatus.custom_status(camera, device))
        # await cam.expose(exptime=exptime, filename=paths[i], write=True)
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Expose Done")
    
    # print(status)
    hdus = []
    dates = []
    for i in range(num):
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Make HDUlist Start")
        hdu = exps[i].to_hdu()[0]

        # hdus.append(hdu)
        dates.append(hdu.header['DATE-OBS'])
        # hdu.header['TEST'] = "TEST"
        for item in list(status[i].items()):
            hdr = item[0] 
            val = item[1]
            # print(hdr, len(val))
            if len(val) > 70:
                continue
            _hdr = hdr.replace(" ", "")
            _hdr = _hdr.replace(".", "")
            _hdr = _hdr.upper()[:8]
            hdu.header[_hdr] = (val, hdr)
        hdus.append(hdu)
        command.info(f"FITS NUMBER={i+1}, EXPTIME={exptime}, Make HDUlist Done")

    # for hdu in hdus: print(repr(hdu.header))

    command.info("Start making filenames")
    filepath = os.path.abspath(filepath)
    paths = []
    for i in range(num):
        filename = f'{cam.name}-{dates[i]}.fits'
        paths.append(os.path.join(filepath, filename))
        command.info(f"Ready for {paths[i]}")
        command.info(f"Write start")
        hdus[i].writeto(paths[i])
        command.info(f" Write done")

    # print(con.cam.name)
    # date_obs = hdus[0].header['DATE-OBS']
    # print(date_obs)
    # for i in range(num)
    # await cs.remove_camera(uid=cam.name)
    command.finish(path=paths)
    return