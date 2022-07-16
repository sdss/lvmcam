#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-12
# @Filename: model.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import abc

from typing import Any, Dict, List, Optional, Tuple, Union

from basecam.exposure import Exposure
from basecam.models import (
    Card,
    CardGroup,
    Extension,
    FITSModel,
    HeaderModel,
    MacroCard,
    WCSCards,
)
from clu.legacy.types.pvt import PVT
from sdsstools.time import get_sjd
from sdsstools import get_logger


        #APOTCCCards() if flicamera.OBSERVATORY == "APO" else None,
        #LampCards() if flicamera.OBSERVATORY == "APO" else None,
        #APOCards() if flicamera.OBSERVATORY == "APO" else None,
        #FPSCards(),
    #]
#)

class WeatherCards(MacroCard):
    def macro(self, exposure, context={}):
        self.logger = get_logger("lvm_weathr")
        self.logger.sh.setLevel(0)
        self.logger.debug(f"{context}")
        truss_temp = 42 # weather.get_truss_temp()
        rh = 66 #weather.get_humid()
        dew_point = truss_temp - ((100 - rh) / 5.)
        return [('TEMP', truss_temp, 'Truss temperature (C)'),
                ('RELHUM', rh, 'Relative humidity (%)'),
                ('DEWPOINT', dew_point, 'Dew point temperature (C)')]



lvmcam_header_model = HeaderModel(
    [
        "VCAM",
        "BASECAMV",
        "CAMNAME",
        "CAMUID",
        "IMAGETYP",
        "EXPTIME",
        "EXPTIMEN",
        "STACK",
        "STACKFUN",
        Card(
            "TIMESYS",
            value="TAI",
            comment="The time scale system",
        ),
        Card(
            "DATE-OBS",
            value="{__exposure__.obstime.tai.isot}",
            comment="Date (in TIMESYS) the exposure started",
        ),
        Card(
            "GAIN",
            value="{__exposure__.camera.gain}",
            comment="[ct] Camera gain"
        ),
        Card("CamType", value="{__exposure__.camera.cam_type}", comment="Camera model"),
        Card("CamTemp", value="{__exposure__.camera.temperature}", comment="[C] Camera Temperature"),
        Card(
            "PIXELSC",
            "{__camera__.arcsec_per_pix}",
            "Scale of unbinned pixel on sky [arcsec/pix]",
            default=-999.0,
            type=float,
        ),
        WCSCards(),
        Card(
            "OBSERVAT",
            "{__camera__.site}",
            "Observatory",
            default="",
        ),
        WeatherCards(),
    ]
)



#: A lvmcam FITS model for uncompressed images. Includes a single extension
#: with the raw data and a `.lvmcam_header_model`.
lvmcam_fits_model = FITSModel(
    [
        Extension(
            data="raw",
            header_model=lvmcam_header_model,
            name="PRIMARY"
        )
    ]
)


#: A compressed, lvmcam FITS model. Similar to `.lvmcam_fits_model` but uses
#: ``RICE_1`` compression.
lvmcam_fz_fits_model = FITSModel(
    [
        Extension(
            data="raw",
            header_model=lvmcam_header_model,
            compressed="RICE_1",
            name="PRIMARY",
        )
    ]
)

