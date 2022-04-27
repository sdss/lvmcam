#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import click

from basecam.actor.tools import get_cameras
from . import camera_parser


__all__ = ["status"]


@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
async def status(command, cameras):
    """Returns the status of a camera."""

    try:
        cameras = get_cameras(command, cameras=cameras, fail_command=True)
        if not cameras:  # pragma: no cover
            return command.finish()

        status = {}
        for camera in cameras:
            try:
                status[camera.name] = camera.get_status(update=True)
            except Exception as ex:
                pass
            try:
                status[camera.name]["binning"] = list(await camera.get_binning())
            except Exception as ex:
                pass
            try:
                status[camera.name]["area"] = tuple(await camera.get_image_area())
            except Exception as ex:
                pass
        return command.finish(status)

    except Exception as ex:
        return command.error(error=ex)
