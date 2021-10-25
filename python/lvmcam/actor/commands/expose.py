from __future__ import absolute_import, annotations, division, print_function

import asyncio
import datetime
import functools
import os
import shutil

import click
import numpy as np
from astropy.io import fits
from astropy.time import Time
from click.decorators import command
from clu.command import Command

from lvmcam.actor import modules
from lvmcam.actor.commands import connection, parser
from lvmcam.araviscam import BlackflyCam as blc
from lvmcam.flir import FLIR_Utils as flir


__all__ = ["expose"]


# A debugging aid, demonstrator and simple test run
# This allows to call this file as an executable from the command line.
# The last command line argument must be the name of the camera
# as used in the configuration file.
# Example
#    lvmcam expose [-t] [-e seconds] [-n #] [-v] [-r RAdegrees] [-d Decdegrees]
#       [-K kmirrdegrees] [-f filepath to save] {spec.age|spec.agw|...}
@parser.command()
@click.option("-t", "--testshot", is_flag=True, help="Test shot")
@click.argument("EXPTIME", type=float)
@click.argument("NUM", type=int)
@click.option("-v", "--verbose", is_flag=True)
# right ascension in degrees (as a simple number)
@click.option("-r", "--ra", type=float, help="RA J2000 in degrees", default=None)
# declination in degrees (as a simple number)
@click.option("-d", "--dec", type=float, help="DEC J2000 in degrees", default=None)
# K-mirror angle in degrees
# Note this is only relevant for 3 of the 4 tables/telescopes
@click.option(
    "-K", "--Kmirr", type=float, help="K-mirror angle in degrees", default=0.0
)
# shortcut for site coordinates: observatory
# @click.option("-s", '--site', default="LCO", help="LCO or MPIA or APO or KHU")
@click.option(
    "-f",
    "--filepath",
    type=str,
    default="python/lvmcam/assets",
    help="The path of files to save",
)
# the last argument is mandatory: must be the name of exactly one camera
# as used in the configuration file
@click.argument("CAMNAME", type=str)
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
    """
    Save fits file

    Example
    -------

    .. code-block:: console
    $ clu
    lvmcam connect
    12:17:35.058 lvmcam >
    12:17:40.083 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    12:17:40.092 lvmcam :
    lvmcam connect
    12:17:42.540 lvmcam >
    12:17:42.542 lvmcam e {
        "text": "Cameras are already connected"
    }
    lvmcam disconnect
    12:17:45.700 lvmcam >
    12:17:45.963 lvmcam i {
        "text": "Cameras have been removed"
    }
    12:17:45.970 lvmcam :

    (lvmcam-with-3.9.7) mgjeon@linux:~/lvmcam$ clu
    lvmcam connect
    12:19:54.419 lvmcam >
    12:19:59.431 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    12:19:59.438 lvmcam :
    lvmcam expose 0.1 3 sci.agw
    12:20:05.037 lvmcam >
    12:20:08.447 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/sci.agw-00000009.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/sci.agw-00000010.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/sci.agw-00000011.fits"
        }
    }
    12:20:08.453 lvmcam :
    lvmcam expose -r 10 -d 10 -K 10 0.5 2 sci.agw
    12:20:22.036 lvmcam >
    12:20:25.397 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/sci.agw-00000012.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/sci.agw-00000013.fits"
        }
    }
    12:20:25.402 lvmcam :
    lvmcam expose -t 0.1 1 sci.agw
    12:20:34.706 lvmcam >
    12:20:37.020 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/test.fits"
        }
    }
    12:20:37.025 lvmcam :

    """
    if not connection.camdict:
        return command.error("There are no connected cameras")
    modules.change_dir_for_normal_actor_start(__file__)
    cam = connection.camdict[camname]
    if testshot:
        num = 1
    if cam.name == "test":
        filepath, paths = await expose_test_cam(
            testshot, exptime, num, verbose, filepath, cam
        )
        # for path in paths:
        #     command.write("i", f"{path}")
        path_dict = {i: paths[i] for i in range(len(paths))}
        command.info(PATH=path_dict)
        return command.finish()
    else:
        paths = await expose_real_cam(
            testshot, exptime, num, verbose, ra, dec, kmirr, filepath, camname, cam
        )
        # for path in paths:
        #     command.write("i", f"{path}")
        path_dict = {i: paths[i] for i in range(len(paths))}
        command.info(PATH=path_dict)
        return command.finish()


def get_last_exposure(path):
    try:
        with open(path, "r") as f:
            return int(f.readline())
    except FileNotFoundError:
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)
        with open(path, "w") as f:
            f.write("0")
            return 0


def set_last_exposure(path, num):
    with open(path, "w") as f:
        f.write(str(num))


def time_to_jd(times):
    # times = ["2021-09-07T03:14:43.060", "2021-09-07T04:14:43.060", "2021-09-08T03:14:43.060"]
    t = Time(times, format="isot", scale="utc")
    jd = np.array(np.floor(t.to_value("jd")), dtype=int)
    return jd


def jd_to_folder(path, jd):
    jd = set(jd)
    for j in jd:
        filepath = os.path.abspath(os.path.join(path, str(j)))
        try:
            os.makedirs(filepath)
        except FileExistsError:
            pass


async def expose_real_cam(
    testshot, exptime, num, verbose, ra, dec, kmirr, filepath, camname, cam
):
    if verbose:
        print(modules.current_progress(__file__, "expose function start"))
    exps, hdrs, status = await expose_cam(exptime, num, verbose, cam)

    hdus, dates = make_header_info(
        exptime, num, verbose, ra, dec, kmirr, camname, exps, hdrs, status
    )

    paths = await make_file(testshot, num, verbose, filepath, cam, hdus, dates)

    if verbose:
        print(modules.current_progress(__file__, "expose function done"))
    return paths


async def make_file(testshot, num, verbose, filepath, cam, hdus, dates):
    if verbose:
        print(modules.current_progress(__file__, "Making filename start"))

    configfile, curNum, paths = prepare_write_file(
        testshot, num, verbose, filepath, cam, hdus, dates
    )
    await write_file(testshot, num, verbose, hdus, configfile, curNum, paths)

    if verbose:
        print(modules.current_progress(__file__, "Making filename done"))
    return paths


def prepare_write_file(testshot, num, verbose, filepath, cam, hdus, dates):
    filepath = os.path.abspath(filepath)

    configfile = os.path.abspath(os.path.join(filepath, "last-exposure.txt"))
    curNum = get_last_exposure(configfile)

    jd = time_to_jd(dates)
    jd_to_folder(filepath, jd)

    paths = []
    for i in range(num):
        curNum += 1
        filename = (
            f"{jd[i]}/{cam.name}-{curNum:08d}.fits" if not testshot else "test.fits"
        )
        paths.append(os.path.join(filepath, filename))

        if verbose:
            print(modules.current_progress(__file__, f"Ready for {paths[i]}"))

        # correct fits data/header
        _hdusheader = hdus[i].header
        _hdusdata = hdus[i].data[0]
        primary_hdu = fits.PrimaryHDU(data=_hdusdata, header=_hdusheader)
        hdus[i] = fits.HDUList(
            [
                primary_hdu,
            ]
        )

    return configfile, curNum, paths


async def write_file(testshot, num, verbose, hdus, configfile, curNum, paths):
    for i in range(num):
        if verbose:
            print(modules.current_progress(__file__, "Write start"))

        if not testshot:
            if verbose:
                print(modules.current_progress(__file__, "Normal Shot"))

            writeto_partial = functools.partial(
                hdus[i].writeto, paths[i], checksum=True
            )
        else:
            if verbose:
                print(modules.current_progress(__file__, "Test Shot"))

            writeto_partial = functools.partial(
                hdus[i].writeto, paths[i], checksum=True, overwrite=True
            )
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, writeto_partial)
        set_last_exposure(configfile, curNum)

        if verbose:
            print(modules.current_progress(__file__, "Write done"))


def make_header_info(
    exptime, num, verbose, ra, dec, kmirr, camname, exps, hdrs, status
):
    wcshdr = blc.get_wcshdr(ra, dec, kmirr, connection.csa[0], camname)
    hdus = []
    dates = []
    for i in range(num):
        if verbose:
            print(
                modules.current_progress(
                    __file__, f"#{i+1}, EXP={exptime}, Setting header start"
                )
            )

        hdu = exps[i].to_hdu()[0]
        dates.append(hdu.header["DATE-OBS"])
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
        if wcshdr is not None:
            for wcs in wcshdr:
                headerName = wcs
                headerValue = wcshdr[wcs]
                headerComment = wcshdr.comments[wcs]
                hdu.header[headerName] = (headerValue, headerComment)

        hdus.append(hdu)

        if verbose:
            print(
                modules.current_progress(
                    __file__, f"#{i+1}, EXP={exptime}, Setting header done"
                )
            )

    return hdus, dates


async def expose_cam(exptime, num, verbose, cam):
    camera, device = flir.setup_camera(verbose)
    exps = []
    hdrs = []
    status = []
    for i in range(num):
        if verbose:
            print(
                modules.current_progress(
                    __file__, f"#{i+1}, EXP={exptime}, Expose start"
                )
            )
        exps.append(await cam.expose(exptime=exptime, image_type="object"))
        if verbose:
            print(
                modules.current_progress(
                    __file__, f"#{i+1}, EXP={exptime}, Expose done"
                )
            )

        if verbose:
            print(
                modules.current_progress(
                    __file__, f"#{i+1}, EXP={exptime}, Saving camera info start"
                )
            )
        status.append(await flir.status_for_header(camera, device))
        if verbose:
            print(
                modules.current_progress(
                    __file__, f"#{i+1}, EXP={exptime}, Saving camera info done"
                )
            )

        hdrs.append(cam.header)
    return exps, hdrs, status


async def expose_test_cam(testshot, exptime, num, verbose, filepath, cam):
    dates = []
    for i in range(num):
        dates.append(datetime.datetime.utcnow().isoformat())

    filepath = os.path.abspath(filepath)
    configfile = os.path.abspath(os.path.join(filepath, "last-exposure.txt"))
    curNum = get_last_exposure(configfile)
    jd = time_to_jd(dates)
    jd_to_folder(filepath, jd)

    paths = []
    for i in range(num):
        curNum += 1
        filename = (
            f"{jd[i]}/{cam.name}-{curNum:08d}.fits" if not testshot else "test.fits"
        )
        paths.append(os.path.join(filepath, filename))
        original = os.path.abspath("python/lvmcam/actor/example")
        if not testshot:
            await asyncio.sleep(exptime)
            shutil.copyfile(original, paths[i])

            if verbose:
                print(modules.current_progress(__file__, f"expose for test #={i+1}"))

        else:
            if os.path.exists(paths[i]):
                os.remove(paths[i])
            await asyncio.sleep(exptime)
            shutil.copyfile(original, paths[i])

            if verbose:
                print(
                    modules.current_progress(__file__, "expose for test with testshot")
                )

        set_last_exposure(configfile, curNum)
    return filepath, paths
