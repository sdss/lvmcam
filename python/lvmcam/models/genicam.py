# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: models/camera.py
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

def config_get(config, key, default=None):
    """ DOESNT work for keys with dots !!! """
    def g(config, key, d=None):
        k = key.split('.', maxsplit=1)
        c = config.get(k[0] if not k[0].isnumeric() else int(k[0]))  # keys can be numeric
        return d if c is None else c if len(k) < 2 else g(c, k[1], d) if type(c) is dict else d
    return g(config, key, default)


class GenicamCards(MacroCard):
    def macro(self, exposure, context={}):
        from sdsstools.logger import get_logger
#        logger = get_logger("ScraperParamCards")
#        logger.warning(f"########### {exposure.scraper_store}")

        return [
            ("GenRevX", 
             config_get(exposure.camera.camera_params,'genicam_params.bool.ReverseX'), 
             '[bool] Flip in X'),
            ("GenRevY", 
             config_get(exposure.camera.camera_params,'genicam_params.bool.ReverseX'), 
             '[bool] Flip in Y'),
        ]

