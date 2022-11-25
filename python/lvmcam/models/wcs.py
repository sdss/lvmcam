# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: models/wcs.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import abc
from math import nan, radians, cos ,sin

from datetime import datetime

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

import astropy.coordinates
import astropy.time
import astropy.units as u

from lvmtipo.site import Site
from lvmtipo.siderostat import Siderostat
from lvmtipo.fiber import Fiber
from lvmtipo.target import Target
from lvmtipo.ambient import Ambient
from lvmtipo.kmirror import Kmirror

from astropy.utils import iers
iers.conf.auto_download = False


def config_get(config, key, default=None):
    """ DOESNT work for keys with dots !!! """
    def g(config, key, d=None):
        k = key.split('.', maxsplit=1)
        c = config.get(k[0] if not k[0].isnumeric() else int(k[0]))  # keys can be numeric
        return d if c is None else c if len(k) < 2 else g(c, k[1], d) if type(c) is dict else d
    return g(config, key, default)


# https://learn.astropy.org/tutorials/synthetic-images.html

class WcsCards(MacroCard):
    def macro(self, exposure, context={}):
        logger = get_logger("ScraperParamCards")

        ra_d = exposure.scraper_store.get('ra_h', 0.0)*15
        dec_d = exposure.scraper_store.get('dec_d', 90.0)
        target = Target(astropy.coordinates.SkyCoord(ra=ra_d, dec=dec_d, unit=(u.deg, u.deg)))


        wcs = exposure.camera.actor.sid.to_wcs(
                         exposure.camera.actor.site,
                         target,
                         None,
                         exposure.camera.actor.ambi,
                         exposure.scraper_store.get('km_s', 0.0),
                         exposure.camera.name,
                         config_get(exposure.camera.camera_params, 'genicam_params.bool.ReverseX', False),
                         config_get(exposure.camera.camera_params, 'genicam_params.bool.ReverseY', False),
                         exposure.camera.actor.kmirror,
                         pixsize=exposure.camera.pixsize,
                         bin=exposure.camera.binning[0],
                         wd=exposure.camera.image_area.wd,
                         hd=exposure.camera.image_area.ht)

        return list(wcs.to_header().cards)




