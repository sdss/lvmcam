# @Author: Mingyu Jeon (mgjeon@khu.ac.kr)
# @Date: 2021-08-23
# @Filename: expose.py

from __future__ import absolute_import, annotations, division, print_function
from astropy.time import Time
import numpy as np

import asyncio
import datetime
import functools
import os

import click
from click.decorators import command
from clu.command import Command

from lvmcam.flir.FLIR_Utils import stat4header, Setup_Camera
from lvmcam.actor.commands import parser
from lvmcam.actor.commands.connection import camdict
from lvmcam.araviscam import BlackflyCam as blc
from astropy.io import fits

import datetime
import shutil


def getLastExposure(path):
    try:
        with open(path, "r") as f:
            return int(f.readline())
    except:
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)
        with open(path, "w") as f:
            f.write("0")
            return 0


def setLastExposure(path, num):
    with open(path, "w") as f:
        f.write(str(num))


def time2jd(times):
    # times = ["2021-09-07T03:14:43.060", "2021-09-07T04:14:43.060", "2021-09-08T03:14:43.060"]
    t = Time(times, format='isot', scale='utc')
    jd = np.array(np.floor(t.to_value('jd')), dtype=int)
    return jd


def jd2folder(path, jd):
    jd = set(jd)
    for j in jd:
        filepath = os.path.abspath(os.path.join(path, str(j)))
        try:
            os.makedirs(filepath)
        except FileExistsError:
            pass


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
    return f"{bcolors.WARNING}{bcolors.BOLD}{time}{bcolors.ENDC}"


__all__ = ["expose"]


# import basecam

# from basecam.exposure import ImageNamer
# image_namer = ImageNamer(
#     "{camera.name}-{num:08d}.fits",
#     dirname=".",
#     overwrite=False,
# )

@parser.command()
@click.argument("EXPTIME", type=float)
@click.argument('NUM', type=int)
@click.argument('CAMNAME', type=str)
@click.argument("FILEPATH", type=str, default="python/lvmcam/assets")
@click.option('--test', is_flag=True, help="testshot")
async def expose(
    command: Command,
    exptime: float,
    num: int,
    camname: str,
    filepath: str,
    test: bool,
):
    if(not camdict):
        command.error(error="There are no connected cameras")
        return
    cam = camdict[camname]
    if (test):
        num = 1
    if(cam.name == "test"):
        dates = []
        for i in range(num):
            dates.append(datetime.datetime.utcnow().isoformat())

        filepath = os.path.abspath(filepath)
        configfile = os.path.abspath(os.path.join(filepath, "last-exposure.txt"))
        curNum = getLastExposure(configfile)
        jd = time2jd(dates)
        jd2folder(filepath, jd)

        paths = []
        for i in range(num):
            curNum += 1
            filename = f"{jd[i]}/{cam.name}-{curNum:08d}.fits" if not test else "test.fits"
            paths.append(os.path.join(filepath, filename))
            original = os.path.abspath("python/lvmcam/actor/example")
            if (not test):
                shutil.copyfile(original, paths[i])
            else:
                if os.path.exists(paths[i]):
                    os.remove(paths[i])
                shutil.copyfile(original, paths[i])
            setLastExposure(configfile, curNum)
        command.finish(path=paths)
        return
    else:
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | expose function start")
        camera, device = Setup_Camera(True)
        exps = []
        hdrs = []
        status = []
        for i in range(num):
            print(f"{pretty2(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Expose start")
            exps.append(await cam.expose(exptime=exptime, image_type="object"))
            print(f"{pretty2(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Expose done")
            print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Saving camera info start")
            status.append(await stat4header(camera, device))
            print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Saving camera info done")
            hdrs.append(cam.header)
            # hdr = exp[0].
            # hdrs.append(hdr)
            # await cam.expose(exptime=exptime, filename=paths[i], write=True)

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

        configfile = os.path.abspath(os.path.join(filepath, "last-exposure.txt"))
        curNum = getLastExposure(configfile)

        jd = time2jd(dates)
        jd2folder(filepath, jd)

        paths = []
        for i in range(num):
            curNum += 1
            filename = f"{jd[i]}/{cam.name}-{curNum:08d}.fits" if not test else "test.fits"
            paths.append(os.path.join(filepath, filename))
            print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Ready for {paths[i]}")
            # correct fits data/header
            _hdusheader = hdus[i].header
            _hdusdata = hdus[i].data[0]
            primary_hdu = fits.PrimaryHDU(data=_hdusdata, header=_hdusheader)
            hdus[i] = fits.HDUList([primary_hdu,])
            print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Write start")
            if (not test):
                writeto_partial = functools.partial(
                    hdus[i].writeto, paths[i], checksum=True
                )
            else:
                writeto_partial = functools.partial(
                    hdus[i].writeto, paths[i], checksum=True, overwrite=True
                )
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, writeto_partial)
            setLastExposure(configfile, curNum)
            print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Write done")
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Making filename done")
        command.finish(path=paths)
        print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | expose function done")
        return
