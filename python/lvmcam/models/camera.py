# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: models/camera.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from basecam.models import Card, CardGroup


CameraCards = CardGroup(
    [
        Card(
            "OBSERVAT",
            value="LCO",
            comment="Observatory",
        ),
        Card(
            "TELESCOP",
            value="{__exposure__.camera.telescope}",
            comment="Telescope that took the image",
        ),
        Card(
            "LMST",
            value="round(__exposure__.obstime.sidereal_time('mean').value, 6)",
            comment="[hr] Local mean sidereal time (approximate)",
            evaluate=True,
        ),
        Card(
            "INSTRUME",
            value="LVM",
            comment="SDSS-V Local Volume Mapper",
        ),
        Card(
            "GAIN",
            value="{__exposure__.camera.gain}",
            comment="[ct] Camera gain",
        ),
        Card(
            "BINX",
            value="{__exposure__.camera.binning[0]}",
            comment="[pix] Binning along axis 1",
        ),
        Card(
            "BINY",
            value="{__exposure__.camera.binning[1]}",
            comment="[pix] Binning along axis 2",
        ),
        Card(
            "CamType",
            value="{__exposure__.camera.cam_type}",
            comment="Camera model",
        ),
        Card(
            "CamTemp",
            value="{__exposure__.camera.temperature}",
            comment="[degC] Camera Temperature",
        ),
        Card(
            "PIXSIZE",
            "{__exposure__.camera.pixsize:.3f}",
            comment="[um] Pixel size",
            default=-999.0,
            type=float,
        ),
        Card(
            "PIXSCALE",
            "{__exposure__.camera.arcsec_per_pix}",
            comment="[arcsec/pix] Scale of unbinned pixel on sky",
            default=-999.0,
            type=float,
        ),
    ]
)
