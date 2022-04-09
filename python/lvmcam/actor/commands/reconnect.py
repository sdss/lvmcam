#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: reconnect.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import asyncio

import click

from basecam.exceptions import CameraConnectionError

from basecam.actor.tools import get_cameras

from . import camera_parser

__all__ = ["reconnect"]


@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
@click.option(
    "--timeout",
    "-t",
    type=float,
    default=5.0,
    show_default=True,
    help="Seconds to wait until disconnect or reconnect command times out.",
)
async def reconnect(command, cameras, timeout):
    """Reconnects a camera."""

    cameras = get_cameras(command, cameras=cameras, fail_command=True)
    if not cameras:  # pragma: no cover
        return

    failed = False
    for camera in cameras:

        command.warning(text=f"reconnecting camera {camera.name!r}")

        try:
            await asyncio.wait_for(camera.disconnect(), timeout=timeout)
            command.info(
                camera=camera.name, text=f"camera {camera.name!r} was disconnected."
            )
        except CameraConnectionError as ee:
            command.warning(
                camera=camera.name,
                text=f"camera {camera.name!r} fail to disconnect: "
                f"{ee}. Will try to reconnect.",
            )
        except asyncio.TimeoutError:
            command.warning(
                camera=camera.name,
                text=f"camera {camera.name!r} timed out "
                "disconnecting. Will try to reconnect.",
            )

        try:
            await asyncio.wait_for(camera.connect(force=True), timeout=timeout)
            command.info(
                camera=camera.name, error=f"camera {camera.name!r} was reconnected."
            )
        except CameraConnectionError as ee:
            command.error(
                camera=camera.name,
                error=f"camera {camera.name!r} fail to reconnect: {ee}",
            )
            failed = True
        except asyncio.TimeoutError:
            command.error(
                camera=camera.name,
                error=f"camera {camera.name!r} timed out reconnecting.",
            )
            failed = True

    if failed:
        return command.fail("some cameras failed to reconnect.")
    else:
        return command.finish()
