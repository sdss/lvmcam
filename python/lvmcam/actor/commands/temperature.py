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

__all__ = ["temperature"]


@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
@click.argument("TEMPERATURE", type=float, required=False)
async def temperature(command, cameras, temperature):
    """Controls the camera temperature.

    If called without a temperature value, returns the current temperature.
    """

    cameras = get_cameras(command, cameras=cameras, fail_command=True)
    if not cameras:  # pragma: no cover
        return

    temperature_tasks = []

    status = {}
    for camera in cameras:
        if not temperature:
            #command.info(
                #temperature=dict(
                    #camera=camera.name,
                    #ccd_temp=await camera.get_temperature(),
                #)
            #)
            status[camera.name] = {"ccd_temp": await camera.get_temperature()}
        else:
            temperature_tasks.append(camera.set_temperature(temperature))
    command.info(status)

    if not temperature:
        return command.finish()

    results = await asyncio.gather(*temperature_tasks, return_exceptions=True)
    failed = False
    for ii, result in enumerate(results):
        if isinstance(result, CameraError):
            command.error(error=dict(camera=cameras[ii].name, error=str(result)))
            failed = True
        else:
            #command.info(
                #temperature=dict(
                    #camera=cameras[ii].name,
                    #ccd_temp=await cameras[ii].get_temperature(),
                #)
            #)
            status[camera.name] = {"ccd_temp": await camera.get_temperature()}

    if failed:
        return command.fail(status)
    else:
        return command.finish(status)
