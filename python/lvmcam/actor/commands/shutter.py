#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: shutter.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import click

from basecam.exceptions import CameraError

from basecam.actor.tools import get_cameras
from . import camera_parser

__all__ = ["shutter"]

@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
@click.option("--open", "shutter_position", flag_value="open", help="Open the shutter.")
@click.option(
    "--close", "shutter_position", flag_value="close", help="Close the shutter."
)
async def shutter(command, cameras, shutter_position):
    """Controls the camera shutter.

    If called without a shutter position flag, returns the current position
    of the shutter.
    """

    try:
        cameras = get_cameras(command, cameras=cameras, fail_command=True)
        if not cameras:  # pragma: no cover
            return

        failed = False
        status = {}
        for camera in cameras:
            if not hasattr(camera,"get_shutter"):
                status[camera.name] = {"shutter": "unavailable"}
                continue
                
            if shutter_position is None:
                shutter_now = await camera.get_shutter()
                status[camera.name] = {"shutter": "open" if shutter_now else "closed"}
            else:
                try:
                    await camera.set_shutter(shutter_position == "open")
                    status[camera.name] = {"shutter": "open" if shutter_now else "closed"}

                except CameraError as ee:
                    status[camera.name] = {"shutter": "unknown"}
                    failed = True

        if failed:
            return command.fail(status)
        else:
            return command.finish(status)

    except Exception as ex:
        return command.error(error=ex)
