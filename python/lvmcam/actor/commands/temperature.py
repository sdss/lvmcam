#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: temperature.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio

import click

from basecam.exceptions import CameraError

from basecam.actor.tools import get_cameras

from . import camera_parser

from math import nan

__all__ = ["temperature"]


@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
@click.argument("TEMPERATURE", type=float, required=False)
async def temperature(command, cameras, temperature):
    """Controls the camera temperature.

    If called without a temperature value, returns the current temperature.
    """

    try:
        cameras = get_cameras(command, cameras=cameras, fail_command=True)
        if not cameras:  # pragma: no cover
            return

        temperature_tasks = []

        status = {}
        for camera in cameras:
            if not hasattr(camera,"get_temperature"):
                status[camera.name] = {"temperature": nan}
                continue

            if not temperature:
                status[camera.name] = {"ccd_temp": await camera.get_temperature()}
            else:
                temperature_tasks.append(camera.set_temperature(temperature))
                command.info(status)

        if not temperature:
            return command.finish(status)

        results = await asyncio.gather(*temperature_tasks, return_exceptions=True)
        failed = False
        for ii, result in enumerate(results):
            if isinstance(result, CameraError):
                command.error(error=dict(camera = cameras[ii].name, error=str(result)))
                failed = True
            else:
                status[camera.name] = {"ccd_temp": await camera.get_temperature()}

        if failed:
            return command.fail(status)
        else:
            return command.finish(status)

    except Exception as ex:
        return command.error(error=ex)
