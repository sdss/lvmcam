from __future__ import absolute_import, annotations, division, print_function

import asyncio
# import datetime
# import functools
import os
import shutil
import ast

# import astropy
import basecam.exposure as base_exp
# import basecam.models.builtin as builtin
import basecam.models.card as card
import basecam.models.fits as fits
import click
# import numpy as np
# from astropy.io import fits
# from astropy.time import Time
from basecam.actor.commands import camera_parser as parser
# from click.decorators import command
from clu.command import Command

from lvmcam.actor import modules
# from lvmcam.actor.commands import connection
from lvmcam.araviscam import BlackflyCam as blc
from lvmcam.flir import FLIR_Utils as flir


__all__ = ["expose"]


@parser.command()
@click.option("-t", "--testshot", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("-eh", "--extraheader", is_flag=True)
@click.option(
    "-h",
    "--header",
    type=str,
    default="{}",
)
# compression option
@click.option(
    "-c",
    "--compress",
    type=click.Choice(["NO", "R1", "RO", "P1", "G1", "G2", "H1"], case_sensitive=True),
)
# @click.option("-p", "--filepath", type=str, default="python/lvmcam/assets")
# right ascension
@click.option("-r", "--ra", default=None)
# declination
@click.option("-d", "--dec", default=None)
# K-mirror angle in degrees
# Note this is only relevant for 3 of the 4 tables/telescopes
@click.option("-K", "--kmirr", type=float, default=None)
# focal length of telescope in mm
# Default is the LCO triple lens configuration of 1.8 meters
@click.option("-f", "--flen", type=float, default=None)
@click.argument("EXPTIME", type=float)
@click.argument("NUM", type=int)
# the last argument is mandatory: must be the name of exactly one camera
# as used in the configuration file
@click.argument("CAMNAME", type=str)
async def expose(
    command: Command,
    testshot: bool,
    verbose: bool,
    # filepath: str,
    ra,
    dec,
    kmirr: float,
    flen: float,
    compress: click.Choice,
    extraheader: bool,
    header: str,
    exptime: float,
    num: int,
    camname: str,
):
    """
    Expose ``num`` times and write the images to a FITS file.

    Parameters
    ----------
    testshot
        Test shot on or off
    verbose
        Verbosity on or off
    ra
        RA J2000 in degrees or in xxhxxmxxs format
    dec
        DEC J2000 in degrees or in +-xxdxxmxxs format
    kmirr
        Kmirr angle in degrees (0 if up, positive with right hand rule along North on bench)
    flen
        focal length of telescope/siderostat in mm
        If not provided it will be taken from the configuration file
    compress
        The option of compression. One of 'None', 'RICE_1', 'RICE_ONE', 'PLIO_1', 'GZIP_1', 'GZIP_2', 'HCOMPRESS_1'.
    extraheader
        Extra header in camera.yaml on or off.
    header
        JSON string with additional header keyword-value pairs. Avoid using spaces.
    exptime
        The exposure time in seconds. Non-negative.
    num
        The number of exposure times. Natural number.
    camname
        The name of camera to expose.
    """
    if not modules.variables.camdict:
        command.error("There are no connected cameras")
        return command.fail()

    modules.change_dir_for_normal_actor_start(__file__)

    if verbose:
        modules.logger.sh.setLevel(int(verbose))
    else:
        modules.logger.sh.setLevel(modules.logging.WARNING)

    cam = modules.variables.camdict[camname]
    modules.variables.camname = camname
    modules.variables.kmirr = kmirr
    modules.variables.flen = flen
    targ = modules.make_targ_from_ra_dec(ra, dec)
    modules.variables.targ = targ
    # print(modules.variables.targ is not None)

    if testshot:
        num = 1

    paths = await expose_cam(
        testshot,
        exptime,
        num,
        cam,
        compress,
        extraheader,
        header,
    )
    path_dict = {i: paths[i] for i in range(len(paths))}
    return command.finish(PATH=path_dict)


@modules.atimeit
async def expose_cam(
    testshot,
    exptime,
    num,
    cam,
    compress,
    extraheader,
    header
):
    path = modules.variables.config['cameras'][modules.variables.camname]['path']
    basename = path['basename']
    dirname = path['dirname']
    filepath = os.path.abspath(path['filepath'])
    dirname = os.path.join(filepath, dirname)

    if compress == 'R1':
        comp = 'RICE_1'
    elif compress == 'RO':
        comp = 'RICE_ONE'
    elif compress == 'P1':
        comp = 'PLIO_1'
    elif compress == 'G1':
        comp = 'GZIP_1'
    elif compress == 'G2':
        comp = 'GZIP_2'
    elif compress == 'H1':
        comp = 'HCOMPRESS_1'
    else:
        comp = False

    hdrlist = [
        "CAMNAME",
        "CAMUID",
        "IMAGETYP",
        "EXPTIME",
        card.Card("DATE-OBS", value="{__exposure__.obstime.tai.isot}", comment="Date (in TIMESYS) the exposure started"),
    ]

    if modules.variables.Aravis_available_camera != {}:
        hdrlist.append(flir.CamCards())

    if (modules.variables.targ is not None) and (modules.variables.kmirr is not None) and (modules.variables.flen is not None):
        hdrlist.append(blc.WcsHdrCards())

    if extraheader:
        config = modules.variables.config
        cg = card.CardGroup(config['cameras'][modules.variables.camname]['extrahdr'])
        hdrlist.append(cg)

    if header != "{}":
        ehdr_dict = ast.literal_eval(header)
        ehdr_list = [[key] + list(value) for key, value in ehdr_dict.items()]
        ehdr_cg = card.CardGroup(ehdr_list)
        hdrlist.append(ehdr_cg)

    hdr_ = fits.HeaderModel(hdrlist)
    fits_model = fits.FITSModel([fits.Extension(header_model=hdr_, name="PRIMARY", compressed=comp)])

    paths = []
    for i in range(num):
        image_namer = base_exp.ImageNamer(basename=basename, dirname=dirname)
        img_path = str(image_namer(cam))

        if testshot:
            img_path = f"{filepath}/testshot.fits"
            if os.path.exists(img_path):
                os.remove(img_path)

        try:
            await cam.expose(exptime=exptime,
                             fits_model=fits_model,
                             image_type="object", write=True,
                             filename=img_path)
        except RuntimeError as err:
            os.remove(img_path)
            img_path = str(err)

        paths.append(img_path)

    return paths
