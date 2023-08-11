#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-08-11
# @Filename: reconnect.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio

import click

from basecam.exceptions import CameraConnectionError
from clu.parsers.click import CluCommand

from lvmcam.actor import LVMCamCommand


__all__ = ["reconnect"]


@click.command(cls=CluCommand)
async def reconnect(command: LVMCamCommand):
    """Reconnects the cameras."""

    # This is specific for lvmcam. We know the cameras that the actor should
    # connect to and we can reconnect them directly. This also helps when the
    # actor has been loaded without any cameras presents. Since the cameras are
    # not autodiscoverable, we have no way to reconnect them other than restarting
    # the actor.

    # Now connect all cameras.
    camera_system = command.actor.camera_system
    assert isinstance(camera_system._config, dict)

    for camera_name in camera_system._config:
        camera = camera_system.get_camera(camera_name)
        if camera:
            command.warning(text=f"reconnecting camera {camera.name!r}")

            try:
                await asyncio.wait_for(camera.disconnect(), timeout=5.0)
                await camera_system.remove_camera(camera_name)

                command.info(
                    camera=camera.name,
                    text=f"camera {camera.name!r} was disconnected.",
                )
            except CameraConnectionError as ee:
                command.warning(
                    camera=camera.name,
                    text=f"camera {camera.name!r} failed to disconnect: "
                    f"{ee}. Will try to reconnect.",
                )
            except asyncio.TimeoutError:
                command.warning(
                    camera=camera.name,
                    text=f"camera {camera.name!r} timed out "
                    "disconnecting. Will try to reconnect.",
                )

        try:
            cam = await camera_system.add_camera(name=camera_name, actor=command.actor)
            command.info(f"Camera {camera_name} connected")

            cam.fits_model.context.update({"__actor__": command.actor})
        except Exception as ex:
            command.error(f"Camera {camera_name} failed connecting: {ex}")

    return command.finish()
