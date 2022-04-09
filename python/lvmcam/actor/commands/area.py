#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: area.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import click

from basecam.exceptions import CameraError

from basecam.actor.tools import get_cameras

from . import camera_parser

__all__ = ["area"]


@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
@click.argument("AREA", nargs=4, type=int, required=False)
@click.option(
    "--reset",
    "-r",
    is_flag=True,
    default=False,
    show_default=True,
    help="Restores the original image area.",
)
async def area(command, cameras, area, reset):
    """Controls the camera image area.

    If called without an image area value, returns the current value.
    The image area must have the format (x0, x1, y0, y1) and be 1-indexed.
    """

    cameras = get_cameras(command, cameras=cameras, fail_command=True)
    if not cameras:  # pragma: no cover
        return

    status={}
    failed = False
    for camera in cameras:
        if not area and reset is False:
            #report_area(command, camera, tuple(await camera.get_image_area()))
            area = await camera.get_image_area()
            status[camera.name]={"area": area}
        else:
            if reset:
                area = None
            try:
                await camera.set_image_area(area)
                status[camera.name]={"area": tuple(await camera.get_image_area())}
            except CameraError as ee:
                command.error(error=dict(camera=camera.name, error=str(ee)))
                failed = True

    if failed:
        return command.fail(status)
    else:
        return command.finish(status)
