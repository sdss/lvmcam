# @Author: Mingyu Jeon (mgjeon@khu.ac.kr)
# @Date: 2021-08-23
# @Filename: expose.py
# @Reference: https://github.com/sdss/araviscam

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
from lvmcam.actor.commands.connection import camdict, csa
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

# A debugging aid, demonstrator and simple test run
# This allows to call this file as an executable from the command line.
# The last command line argument must be the name of the camera
# as used in the configuration file.
# Example
#    lvmcam expose [-t] [-e seconds] [-n #] [-v] [-r RAdegrees] [-d Decdegrees] 
#       [-K kmirrdegrees] [-f filepath to save] {spec.age|spec.agw|...}
@parser.command()
@click.option("-t", '--testshot', is_flag=True, help="Test shot")

@click.argument("EXPTIME", type=float)

@click.argument("NUM", type=int)

@click.option("-v", '--verbose', is_flag=True)

# right ascension in degrees (as a simple number)
@click.option("-r", '--ra', type=float, help="RA J2000 in degrees", default=None)

# declination in degrees (as a simple number)
@click.option("-d", '--dec', type=float, help="DEC J2000 in degrees", default=None)

# K-mirror angle in degrees 
# Note this is only relevant for 3 of the 4 tables/telescopes
@click.option("-K", '--Kmirr', type=float, help="K-mirror angle in degrees", default=0.0)

# shortcut for site coordinates: observatory
# @click.option("-s", '--site', default="LCO", help="LCO or MPIA or APO or KHU")

@click.option("-f", '--filepath', type=str, default="python/lvmcam/assets", help="The path of files to save")

# the last argument is mandatory: must be the name of exactly one camera
# as used in the configuration file
@click.argument('CAMNAME', type=str)
async def expose(
    command: Command,
    testshot: bool,
    exptime: float,
    num: int,
    verbose: bool,
    ra: float,
    dec: float,
    kmirr: float,
    filepath: str,
    camname: str,
):
    if(not camdict):
        command.error(error="There are no connected cameras")
        return
    cam = camdict[camname]
    if (testshot):
        num = 1
    if(cam.name == "test"):
        dates = []
        for i in range(num):
            dates.append(datetime.datetime.utcnow().isoformat())

        os.chdir(os.path.dirname(__file__))
        os.chdir('../')
        os.chdir('../')
        os.chdir('../')
        os.chdir('../')
        filepath = os.path.abspath(filepath)
        configfile = os.path.abspath(os.path.join(filepath, "last-exposure.txt"))
        curNum = getLastExposure(configfile)
        jd = time2jd(dates)
        jd2folder(filepath, jd)

        paths = []
        for i in range(num):
            curNum += 1
            filename = f"{jd[i]}/{cam.name}-{curNum:08d}.fits" if not testshot else "test.fits"
            paths.append(os.path.join(filepath, filename))
            original = os.path.abspath("python/lvmcam/actor/example")
            if (not testshot):
                await asyncio.sleep(exptime)
                shutil.copyfile(original, paths[i])

                if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | expose for test #={i+1}") 

            else:
                if os.path.exists(paths[i]):
                    os.remove(paths[i])
                await asyncio.sleep(exptime)
                shutil.copyfile(original, paths[i])

                if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | expose for test with testshot") 

            setLastExposure(configfile, curNum)
        command.finish(path=paths)
        return
    else:

        if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | expose function start") 

        camera, device = Setup_Camera(verbose)
        exps = []
        hdrs = []
        status = []
        for i in range(num):

            if verbose : print(f"{pretty2(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Expose start") 

            exps.append(await cam.expose(exptime=exptime, image_type="object"))

            if verbose : print(f"{pretty2(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Expose done") 
            if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Saving camera info start") 

            status.append(await stat4header(camera, device))

            if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Saving camera info done") 

            hdrs.append(cam.header)
            # hdr = exp[0].
            # hdrs.append(hdr)
            # await cam.expose(exptime=exptime, filename=paths[i], write=True)
        
        # print(csa[0])
        wcshdr = blc.get_wcshdr(ra, dec, kmirr, csa[0], camname)
        # print(repr(wcshdr))
        # for wcs in wcshdr:
        #     print(wcs, wcshdr[wcs], wcshdr.comments[wcs])

        # print(status)
        hdus = []
        dates = []
        for i in range(num):

            if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Setting header start") 

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
            if(wcshdr != None):
                for wcs in wcshdr:
                    headerName = wcs
                    headerValue = wcshdr[wcs]
                    headerComment = wcshdr.comments[wcs]
                    hdu.header[headerName] = (headerValue, headerComment)
                # print(wcs, wcshdr[wcs], wcshdr.comments[wcs])
            
            hdus.append(hdu)

            if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | #{i+1}, EXP={exptime}, Setting header done") 

        # for hdu in hdus: print(repr(hdu.header))

        if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Making filename start") 

        filepath = os.path.abspath(filepath)

        configfile = os.path.abspath(os.path.join(filepath, "last-exposure.txt"))
        curNum = getLastExposure(configfile)

        jd = time2jd(dates)
        jd2folder(filepath, jd)

        paths = []
        for i in range(num):
            curNum += 1
            filename = f"{jd[i]}/{cam.name}-{curNum:08d}.fits" if not testshot else "test.fits"
            paths.append(os.path.join(filepath, filename))

            if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Ready for {paths[i]}") 

            # correct fits data/header
            _hdusheader = hdus[i].header
            _hdusdata = hdus[i].data[0]
            primary_hdu = fits.PrimaryHDU(data=_hdusdata, header=_hdusheader)
            hdus[i] = fits.HDUList([primary_hdu,])

            if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Write start") 

            if (not testshot):

                if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Normal Shot") 

                writeto_partial = functools.partial(
                    hdus[i].writeto, paths[i], checksum=True
                )
            else:

                if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Test Shot") 

                writeto_partial = functools.partial(
                    hdus[i].writeto, paths[i], checksum=True, overwrite=True
                )
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, writeto_partial)
            setLastExposure(configfile, curNum)

            if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Write done") 

        if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | Making filename done") 

        command.finish(path=paths)

        if verbose : print(f"{pretty(datetime.datetime.now())} | lvmcam/expose.py | expose function done") 
        return
