#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-09-11
# @Filename: proc.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from basecam.models import Card, CardGroup


ProcCards = CardGroup(
    [
        Card(
            "TELESCOP",
            value="{__exposure__.camera.telescope}",
            comment="Telescope that took the image",
        ),
        "CAMNAME",
        Card(
            "DARKFILE",
            value=None,
            comment="Associated dark frame",
        ),
        Card(
            "DIRNAME",
            value=None,
            comment="Original file directory",
        ),
        Card(
            "GUIDERV",
            value="0.0.0",
            comment="Version of lvmguider",
        ),
        Card(
            "SOURCESF",
            value=None,
            comment="Sources file",
        ),
        Card(
            "FWHM",
            value=None,
            comment="[arcsec] FWHM from sources",
        ),
        Card(
            "RA",
            value=None,
            comment="[deg] RA of central pixel from WCS",
        ),
        Card(
            "DEC",
            value=None,
            comment="[deg] Dec of central pixel from WCS",
        ),
        Card(
            "PA",
            value=None,
            comment="[deg] Position angle from WCS",
        ),
        Card(
            "ZEROPT",
            value=None,
            comment="[mag] Zero point of the LVM magnitude",
        ),
        Card(
            "ORIGFILE",
            value=None,
            comment="Original file name",
        ),
        Card(
            "REPROC",
            value=False,
            comment="Has this file been reprocessed?",
        ),
        Card(
            "REFFILE",
            value=None,
            comment="Astrom. solution ref. file",
        ),
        Card(
            "ISFSWEEP",
            value=False,
            comment="Is the exposure part of a focus sweep?",
        ),
        Card(
            "SOLVED",
            value=False,
            comment="Was an astrometric solution found?",
        ),
        Card(
            "WCSMODE",
            value="none",
            default="none",
            comment="Method for fitting the astrometric solution",
        ),
    ]
)
