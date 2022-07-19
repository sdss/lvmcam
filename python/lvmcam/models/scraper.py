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
from clu.legacy.types.pvt import PVT
from sdsstools.time import get_sjd
from sdsstools import get_logger

class ScraperParamCards(MacroCard):
    def macro(self, exposure, context={}):
        
        return [
            ('RA', exposure.camera.params.get('ra_h', 0.0)*15, '[deg] Right Ascension of the observation'),
            ('DEC', exposure.camera.params.get('dec_d', 90.0), '[deg] Declination of the observation'),
            ('FIELDROT', exposure.camera.params.get('field_angle_degs', -999.9), '[deg] Field angle from PW'),
            ('KMIRDROT', exposure.camera.params.get('km_d', -999.9), '[deg] Rotation angle kmirror'),
            ('FOCUSUM', exposure.camera.params.get('foc_um', -999.9), '[um] Focus stage position'),
        ]

