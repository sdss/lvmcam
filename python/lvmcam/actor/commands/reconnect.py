#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: reconnect.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import asyncio

import click

from cluplus.proxy import Proxy

from basecam.exceptions import CameraConnectionError

from basecam.actor.tools import get_cameras

from lvmcam.exceptions import LvmcamNotConnected

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

    try:
        cameras = get_cameras(command, cameras=cameras, fail_command=True)

        failed = False
        status = {}
        for camera in cameras:
            try:
                await asyncio.wait_for(camera.disconnect(), timeout=timeout)
                status[camera.name] = {"state": "offline"}

            except CameraConnectionError as ee:
                status[camera.name] = {"state": "unknown", "error": Proxy._exceptionToMap(ee)}
                continue

            except asyncio.TimeoutError as ee:
                status[camera.name] = {"state": "unknown", "error": Proxy._exceptionToMap(ee)}
                continue

            try:
                await asyncio.wait_for(camera.connect(force=True), timeout=timeout)
                status[camera.name] = {"state": "online"}

            except CameraConnectionError as ee:
                status[camera.name] = {"state": "unknown", "error": Proxy._exceptionToMap(ee)}
                failed = True
                continue

            except asyncio.TimeoutError as ee:
                status[camera.name] = {"state": "unknown", "error": Proxy._exceptionToMap(ee)}
                failed = True
                continue

        if failed:
            raise LvmcamNotConnected(status)

        command.finish(status)

    except Exception as ex:
        return command.fail(error=ex)

