#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: gain.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import click

from clu.parsers.click import CluCommand

from basecam.exceptions import CameraError

from basecam.actor.tools import get_cameras

from . import camera_parser

__all__ = ["gain"]

@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
@click.argument("GAIN", nargs=1, type=int, required=False)
async def gain(command, cameras, gain):
    """Controls the camera gain.

    If called without a gain value, returns the current value.
    """

    try:
        cameras = get_cameras(command, cameras=cameras, fail_command=True)
        if not cameras:  # pragma: no cover
            return

        failed = False

        status = {}
        for camera in cameras:
            if not gain:
                gain = await camera.get_gain()
                status[camera.name] = { "gain": gain }
            else:
                try:
                    await camera.set_gain(gain)
                    status[camera.name] = { "gain": gain }

                except (CameraError, AssertionError) as ee:
                    command.error(error=ee)
                    failed = True

        if failed:
            return command.fail("failed to set gain for one or more cameras.")
        else:
            return command.finish(status)

    except Exception as ex:
        return command.error(error=ex)
