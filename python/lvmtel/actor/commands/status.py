#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio

import click
from . import parser


__all__ = ["status"]

def statusSensorRead(sensor):

    data = sensor.readline().split()

#    print(data)

    status = {}
    status["temperature"] = float(data[0])
    status["humidity"] = float(data[2])
    status["pressure"] = float(data[4])

    return status


async def statusTick(command, delta_time):

    lock = command.actor.statusLock

    while command.actor.statusTask:
        try:
            if not lock.locked():
                command.actor.write(
                        "i",
                        statusSensorRead(command.actor.sensor)
                )

        except Exception as e:
            command.actor.write("i", {"error": e})
#            print(e)

        await asyncio.sleep(0.5)


@parser.command()
@click.option("--statusTick", type=float, default=5)
async def status(command, statustick:float):
    """Returns the status of a camera."""

    lock = command.actor.statusLock

    try:
        async with lock:
            command.actor.sensor.flushInput()
            status = statusSensorRead(command.actor.sensor)
            command.finish(status)

        if statustick > 0.0:
            if not command.actor.statusTask:
                command.actor.statusTask = command.actor.loop.create_task(statusTick(command, statustick))
        else:
            command.actor.statusTask = None

    except Exception as ex:
        return command.error(error=ex)
