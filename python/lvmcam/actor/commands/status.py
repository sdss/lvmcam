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
from .expose import EXPOSURE_STATE


__all__ = ["status"]


@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
async def status(command, cameras):
    """Returns the status of a camera."""
    global EXPOSURE_STATE

    try:
        cameras = get_cameras(command, cameras=cameras, fail_command=True)
        if not cameras:  # pragma: no cover
            return command.finish()

        status = {}
        for camera in cameras:
            
            status[camera.name] = camera.get_status(update=True)
            status[camera.name]["shutter"] = "open" if await camera.get_shutter() else "closed"
#        status.update(EXPOSURE_STATE)

        return command.finish(status)

    except Exception as ex:
        return command.error(error=ex)
