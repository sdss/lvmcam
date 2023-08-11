# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: models/scraper.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

from araviscam import BlackflyCamera
from basecam.models import MacroCard


if TYPE_CHECKING:
    from python.lvmcam.actor import LVMCamActor


class ScraperParamCards(MacroCard):
    def macro(self, exposure, context={}):
        assert isinstance(exposure.camera, BlackflyCamera)

        actor: LVMCamActor = exposure.camera.actor

        ra_h = actor.scraper_data.get("ra_h", -999.0)
        ra_d = -999.0 if ra_h < 0 else ra_h * 15

        return [
            (
                "RA",
                round(ra_d, 6),
                "[deg] Telescope Right Ascension",
            ),
            (
                "DEC",
                round(actor.scraper_data.get("dec_d", 90.0), 6),
                "[deg] Telescope Declination",
            ),
            (
                "ALT",
                round(actor.scraper_data.get("alt_d", 0.0), 6),
                "[deg] Telescope Altitude",
            ),
            (
                "AZ",
                round(actor.scraper_data.get("az_d", 90.0), 6),
                "[deg] Telescope Azimuth",
            ),
            (
                "FIELDROT",
                round(actor.scraper_data.get("field_angle_d", -999.0), 3),
                "[deg] Cassegrain Field angle from PW",
            ),
            # (
            #     "PWA0POS",
            #     round(actor.scraper_data.get("axis0_position_d", -999.0), 6),
            #     "[deg] Axis0 pos angle from PW",
            # ),
            # (
            #     "PWA0T",
            #     actor.scraper_data.get("axis0_position_timestamp_s", -999.0),
            #     "[] Axis0 pos angle time from PW",
            # ),
            # (
            #     "PWA1POS",
            #     actor.scraper_data.get("axis1_position_d", -999.0),
            #     "[deg] Axis1 pos angle from PW",
            # ),
            # (
            #     "PWA1T",
            #     actor.scraper_data.get("axis1_position_timestamp_s", -999.0),
            #     "[] Axis1 pos angle time from PW",
            # ),
            (
                "KMIRDROT",
                round(actor.scraper_data.get("km_d", -999.0), 3),
                "[deg] K-mirror rotation angle",
            ),
            (
                "KMIRSTEP",
                round(actor.scraper_data.get("km_s", -999.0), 1),
                "[steps] K-mirror motor steps",
            ),
            (
                "FOCUSDT",
                round(actor.scraper_data.get("foc_dt", -999.0), 2),
                "[dt] Focus stage position",
            ),
            (
                "BENTEMPI",
                round(actor.scraper_data.get("bentempi", -999.0), 1),
                "[degC] Temperature bench inside",
            ),
            (
                "BENHUMI",
                round(actor.scraper_data.get("benhumi", -999.0), 1),
                "[%] Humidity bench inside",
            ),
            (
                "BENPRESI",
                actor.scraper_data.get("benpressi", -999.0),
                "[hPa] Pressure bench inside",
            ),
            (
                "BENTEMPO",
                round(actor.scraper_data.get("bentempo", -999.0), 1),
                "[degC] Temperature bench outside",
            ),
            (
                "BENHUMO",
                round(actor.scraper_data.get("benhumo", -999.0), 1),
                "[%] Humidity bench oustside",
            ),
            (
                "BENPRESO",
                actor.scraper_data.get("benpresso", -999.0),
                "[hPa] Pressure bench oustside",
            ),
        ]
