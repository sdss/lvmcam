# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: models/scraper.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from datetime import datetime

from basecam.models import MacroCard
from cluplus.proxy import flatten


class ScraperDataStore(object):
    def __init__(self, actor, config={}):
        self.actor_key_maps = config
        self.data = {}

    def copy(self):
        o = type(self).__new__(self.__class__)
        o.actor_key_maps = self.actor_key_maps.copy()
        o.data = self.data.copy()
        return o

    def __repr__(self):
        return self.data.__repr__()

    def keys(self):
        return self.data.keys()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def actors(self):
        return list(self.actor_key_maps.keys()) if self.actor_key_maps else []

    def set(self, key, val, timestamp=datetime.utcnow()):
        self.data[key] = (val, timestamp)

    def get(self, key, default=None):
        return self.data.get(key, (default, None))[0]

    def update(self, data: dict, timestamp=datetime.utcnow()):
        self.data.update({k: (v, timestamp) for k, v in data.items()})

    def update_with_actor_key_maps(
        self, actor, data: dict, timestamp=datetime.utcnow()
    ):
        akm = self.actor_key_maps.get(actor, None)
        self.data.update(
            {
                akm[k]: (v, timestamp)
                for k, v in flatten(data).items()
                if k in akm.keys()
            }
        )

    def items(self):
        return self.data.items()


def config_get(config, key, default=None):
    """DOESNT work for keys with dots !!!"""

    def g(config, key, d=None):
        k = key.split(".", maxsplit=1)
        c = config.get(
            k[0] if not k[0].isnumeric() else int(k[0])
        )  # keys can be numeric
        return (
            d
            if c is None
            else c
            if len(k) < 2
            else g(c, k[1], d)
            if type(c) is dict
            else d
        )

    return g(config, key, default)


class ScraperParamCards(MacroCard):
    def macro(self, exposure, context={}):
        from sdsstools.logger import get_logger

        logger = get_logger("ScraperParamCards")
        logger.warning(f"########### {exposure.scraper_store}")

        #        logger.warning(f"{config_get(exposure.camera.camera_params,'genicam_params.bool.ReverseX')}")

        return [
            (
                "RA",
                exposure.scraper_store.get("ra_h", 0.0) * 15,
                "[deg] Right Ascension of the observation",
            ),
            (
                "DEC",
                exposure.scraper_store.get("dec_d", 90.0),
                "[deg] Declination of the observation",
            ),
            (
                "ALT",
                exposure.scraper_store.get("alt_d", 0.0),
                "[deg] pointing Altitude telescope",
            ),
            (
                "AZ",
                exposure.scraper_store.get("az_d", 90.0),
                "[deg] pointing Azimuth telescope",
            ),
            (
                "FIELDROT",
                exposure.scraper_store.get("field_angle_d", -999.9),
                "[deg] Cassegrain Field angle from PW",
            ),
            (
                "PWA0POS",
                exposure.scraper_store.get("axis0_position_d", -999.9),
                "[deg] Axis0 pos angle from PW",
            ),
            (
                "PWA0T",
                exposure.scraper_store.get("axis0_position_timestamp_s", -999.9),
                "[] Axis0 pos angle time from PW",
            ),
            (
                "PWA1POS",
                exposure.scraper_store.get("axis1_position_d", -999.9),
                "[deg] Axis1 pos angle from PW",
            ),
            (
                "PWA1T",
                exposure.scraper_store.get("axis1_position_timestamp_s", -999.9),
                "[] Axis1 pos angle time from PW",
            ),
            (
                "KMIRDROT",
                exposure.scraper_store.get("km_d", -999.9),
                "[deg] Rotation angle kmirror",
            ),
            (
                "KMIRSTEP",
                exposure.scraper_store.get("km_s", -999.9),
                "[steps] position kmirror",
            ),
            (
                "FOCUSDT",
                exposure.scraper_store.get("foc_dt", -999.9),
                "[dt] Focus stage position",
            ),
            (
                "BENTEMPI",
                exposure.scraper_store.get("bentempi", -999.9),
                "[degC] Temperature bench inside",
            ),
            (
                "BENHUMO",
                exposure.scraper_store.get("benhumo", -999.9),
                "[] Humidity bench oustside",
            ),
            (
                "BENTEMPO",
                exposure.scraper_store.get("benpresso", -999.9),
                "[hPa] Pressure bench oustside",
            ),
        ]
