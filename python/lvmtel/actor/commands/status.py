#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import click

from . import parser

import serial


__all__ = ["status"]


@parser.command()
async def status(command):
    """Returns the status of a camera."""

    try:
        ser = serial.Serial('/dev/ttyUSB0')

        ser.readline()
        data = ser.readline().split()

        print(data)

        status = {}
        status["temperature"] = float(data[0])
        status["humidity"] = float(data[2])
        status["pressure"] = float(data[4])

        return command.finish(status)

    except Exception as ex:
        return command.error(error=ex)
