# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: models/camera.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from basecam.models import MacroCard


class GenicamCards(MacroCard):
    def macro(self, exposure, context={}):
        genicam_params = exposure.camera.camera_params.get("genicam_params", {})

        return [
            (
                "GenRevX",
                genicam_params.get("bool", {}).get("ReverseX", None),
                "[bool] Flip in X",
            ),
            (
                "GenRevY",
                genicam_params.get("bool", {}).get("ReverseY", None),
                "[bool] Flip in Y",
            ),
        ]
