#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: binning.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import click

from clu.parsers.click import CluCommand

from basecam.exceptions import CameraError

from basecam.actor.tools import get_cameras

from . import camera_parser

__all__ = ["binning"]

@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
@click.argument("BINNING", nargs=2, type=int, required=False)
async def binning(command, cameras, binning):
    """Controls the camera binning.

    If called without a binning value, returns the current value.
    """

    try:
        cameras = get_cameras(command, cameras=cameras, fail_command=True)
        if not cameras:  # pragma: no cover
            return

        failed = False

        status = {}
        for camera in cameras:
            if not binning:
                binning = list(await camera.get_binning())
                status[camera.name] = { "binning": binning }
            else:
                try:
                    await camera.set_binning(*binning)
                    status[camera.name] = { "binning": binning }

                except (CameraError, AssertionError) as ee:
                    command.error(error=dict(camera=camera.name, error=str(ee)))
                    failed = True

        if failed:
            return command.fail("failed to set binning for one or more cameras.")
        else:
            return command.finish(status)

    except Exception as ex:
        return command.error(error=ex)
