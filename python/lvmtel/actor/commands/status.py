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

import gude_sensor

__all__ = ["status"]

def statusSensorRead(sensor):

#    data = sensor.readline().split()
    data = gude_sensor.getSensorsJson("10.8.38.122")

#    print(data)

    status = {}
    status["temperature"] = data['sensor_values'][0]['values'][0][0]['v']
    status["humidity"] = data['sensor_values'][1]['values'][0][1]['v']
    status["temperature_enclosure"] = data['sensor_values'][1]['values'][0][0]['v']
    status["humidity_enclosure"] = data['sensor_values'][1]['values'][0][1]['v']
    status["dewpoint_enclosure"] = data['sensor_values'][1]['values'][0][2]['v']

    return status


async def statusTick(actor, delta_time):

    lock = actor.statusLock

    while actor.statusTask:
        try:
            if not lock.locked():
                actor.write(
                        "i",
                        statusSensorRead(actor.sensor)
                )

        except Exception as e:
            actor.write("i", {"error": e})
#            print(e)

        await asyncio.sleep(delta_time)


@parser.command()
@click.option("--statusTick", type=float, default=5)
async def status(command, statustick:float):
    """Returns the status of a camera."""

    lock = command.actor.statusLock

    try:
        async with lock:
#            command.actor.sensor.flushInput()
            status = statusSensorRead(command.actor.sensor)
            command.finish(status)

        if statustick > 0.0:
            if not command.actor.statusTask:
                command.actor.statusTask = command.actor.loop.create_task(statusTick(command.actor, statustick))
        else:
            command.actor.statusTask = None

    except Exception as ex:
        return command.error(error=ex)
