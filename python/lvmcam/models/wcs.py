# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: models/wcs.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

import astropy.coordinates
import astropy.time
from astropy.utils import iers

from araviscam import BlackflyCamera
from basecam.models import MacroCard
from lvmtipo.ambient import Ambient
from lvmtipo.kmirror import Kmirror
from lvmtipo.siderostat import Siderostat
from lvmtipo.site import Site
from lvmtipo.target import Target


if TYPE_CHECKING:
    from python.lvmcam.actor.actor import LVMCamActor


iers.conf.auto_download = False


class WCSCards(MacroCard):
    """WCS cards for the header."""

    def __init__(
        self,
        name: str | None = None,
        use_group_title: bool = False,
        config: dict = {},
        **kwargs,
    ):
        super().__init__(name=name, use_group_title=use_group_title, **kwargs)

        self.site = Site(name=config.get("site", "LCO"))

        if self.site.lat > 40.0:
            azang = 180  # MPIA
        else:
            azang = 0  # LCO, APO, KHU

        medSign = -1

        self.sidereostat = Siderostat(azang=azang, medSign=medSign)

        homeOffset = 135
        homeIsWest = False

        self.kmirror = Kmirror(home_is_west=homeIsWest, home_offset=homeOffset)

        self.ambient = Ambient()

    def macro(self, exposure, context={}):
        assert isinstance(exposure.camera, BlackflyCamera)

        actor: LVMCamActor = exposure.camera.actor

        genicam_params = exposure.camera.camera_params.get("genicam_params", {})
        reverse_x = genicam_params.get("bool", {}).get("ReverseX", None)
        reverse_y = genicam_params.get("bool", {}).get("ReverseY", None)

        ra_d = actor.scraper_data.get("ra_h", 0.0) * 15
        dec_d = actor.scraper_data.get("dec_d", 90.0)
        target = Target(astropy.coordinates.SkyCoord(ra=ra_d, dec=dec_d, unit="deg"))

        wcs = self.sidereostat.to_wcs(
            self.site,
            target,
            None,
            self.ambient,
            actor.scraper_data.get("km_s", 0.0),
            actor.name + " " + exposure.camera.name,
            reverse_x,
            reverse_y,
            self.kmirror,
            pixsize=exposure.camera.pixsize,
            bin=exposure.camera.binning[0],
            wd=exposure.camera.image_area.wd,
            hd=exposure.camera.image_area.ht,
        )

        return list(wcs.to_header().cards)
