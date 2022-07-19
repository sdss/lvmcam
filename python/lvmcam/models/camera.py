#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-12
# @Filename: model.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import abc
from math import nan

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
from sdsstools.time import get_sjd
from sdsstools import get_logger

#class WeatherCards(MacroCard):
    #def macro(self, exposure, context={}):
        #self.logger = get_logger("lvm_weathr")
        #self.logger.sh.setLevel(0)
        #self.logger.debug(f"{context}")
        #truss_temp = 42 # weather.get_truss_temp()
        #rh = 66 #weather.get_humid()
        #dew_point = truss_temp - ((100 - rh) / 5.)
        #return [('TEMP', truss_temp, 'Truss temperature (C)'),
                #('RELHUM', rh, 'Relative humidity (%)'),
                #('DEWPOINT', dew_point, 'Dew point temperature (C)')]


CameraCards = CardGroup(
    [
        Card("OBSERVAT", "{__camera__.site}", "Observatory", default="",),
        Card("GAIN", value="{__exposure__.camera.gain}", comment="[ct] Camera gain"),
        Card("CamType", value="{__exposure__.camera.cam_type}", comment="Camera model"),
        Card("CamTemp", value="{__exposure__.camera.temperature}", comment="[C] Camera Temperature"),
        Card("PIXELSC", "{__exposure__.camera.arcsec_per_pix}", comment="[arcsec/pix] Scale of unbinned pixel on sky", default=-999.0, type=float),
    ]
)

