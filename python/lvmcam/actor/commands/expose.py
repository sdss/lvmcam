#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: expose.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio
from functools import partial

import click

from basecam.events import CameraEvent
from basecam.exceptions import ExposureError

from basecam.actor.tools import get_cameras
from . import camera_parser

__all__ = ["expose"]


def report_exposure_state(command, event, payload):

    if event not in CameraEvent:
        return

    name = payload.get("name", "")
    if not name:
        return

    command.actor.log.debug(f"report_exposure_state {event} {type(event)} {payload}")


    if name not in command.actor.exposure_state:
        command.actor.exposure_state[name] = {}

    command.actor.exposure_state[name]["state"] = event.value

    command.actor.exposure_state[name].update(payload)

    if event == CameraEvent.EXPOSURE_INTEGRATING:
        pass
    elif event == CameraEvent.EXPOSURE_FLUSHING:
        pass
    elif event == CameraEvent.EXPOSURE_READING:
        command.actor.exposure_state[name].update({"remaining_time": 0.0})
    elif event == CameraEvent.EXPOSURE_DONE:
        command.actor.exposure_state[name].update({"remaining_time": 0.0})
    elif event == CameraEvent.EXPOSURE_FAILED:
        command.actor.exposure_state[name].update(
            {
                "remaining_time": 0.0,
                "current_stack": 0,
                "n_stack": 0,
            }
        )
    elif event == CameraEvent.EXPOSURE_IDLE:
        command.actor.exposure_state[name].update(
            {
                "remaining_time": 0.0,
                "current_stack": 0,
                "n_stack": 0,
                "exptime": 0,
                "image_type": "NA",
            }
        )
        return
    elif event == CameraEvent.EXPOSURE_WRITTEN:
        filename = payload.get("filename", "UNKNOWN")
        info = { name:
          {   
              "state": command.actor.exposure_state[name].get("state", "NA"),
              "filename": filename, 
          }
        }
        command.info(info)
        command.actor.exposure_state[name].update(info)
        return
    elif event == CameraEvent.EXPOSURE_POST_PROCESSING:
        command.info(
          { name:
            {   
              "state": command.actor.exposure_state[name].get("state", "NA"),
              "image_type": command.actor.exposure_state[name].get("image_type", "NA"),
            }
          }
        )
        return
    elif event == CameraEvent.EXPOSURE_POST_PROCESS_FAILED:
        command.warning(
          { name:
             {  
               "state": command.actor.exposure_state[name].get("state", "NA"),
               "image_type": command.actor.exposure_state[name].get("image_type", "NA"),
               "error": payload.get("error", "Error unknown"),
             }
          }
        )
        return
    else:
        return

    command.info(
        { name:
           {
            "state": command.actor.exposure_state[name].get("state", "NA"),
            "image_type": command.actor.exposure_state[name].get("image_type", "NA"),
            "remaining_time": command.actor.exposure_state[name].get("remaining_time", 0),
            "exposure_time": command.actor.exposure_state[name].get("exptime", 0),
            "current_stack": command.actor.exposure_state[name].get("current_stack", 0),
            "n_stack": command.actor.exposure_state[name].get("n_stack", 0),
           }
        }
    )

async def expose_one_camera(
    command,
    camera,
    exptime,
    image_type,
    stack,
    filename,
    no_postprocess,
    **extra_kwargs,
):
    obj = click.get_current_context().obj
    try:
        exposure = await camera.expose(
            exptime,
            image_type=image_type,
            stack=stack,
            filename=filename,
            postprocess=not no_postprocess,
            write=True,
            **extra_kwargs,
        )
        post_process_cb = obj.get("post_process_callback", None)
        if post_process_cb:
            await post_process_cb(command, exposure)
        return True
    except ExposureError as ee:
        command.error(error={"camera": camera.name, "error": str(ee)})
        return False


@camera_parser.command()
@click.argument("CAMERAS", nargs=-1, type=str, required=False)
@click.argument("EXPTIME", type=float, required=True)
@click.option(
    "--object",
    "image_type",
    flag_value="object",
    default=True,
    show_default=True,
    help="Takes an object exposure.",
)
@click.option(
    "--flat",
    "image_type",
    flag_value="flat",
    show_default=True,
    help="Takes a flat exposure.",
)
@click.option(
    "--dark",
    "image_type",
    flag_value="dark",
    show_default=True,
    help="Takes a dark exposure.",
)
@click.option(
    "--bias",
    "image_type",
    flag_value="bias",
    show_default=True,
    help="Takes a bias exposure.",
)
@click.option(
    "--filename",
    "-f",
    type=str,
    default=None,
    show_default=True,
    help="Filename of the imaga to save.",
)
@click.option(
    "--stack",
    "-s",
    type=int,
    default=1,
    show_default=True,
    help="Number of images to stack.",
)
@click.option(
    "--no-postprocess",
    is_flag=True,
    help="Skip the post-process step, if defined.",
)
async def expose(
    command,
    cameras,
    exptime,
    image_type,
    filename,
    stack,
    no_postprocess,
    **exposure_kwargs,
):
    """Exposes and writes an image to disk."""

    try:
        cameras = get_cameras(command, cameras=cameras, fail_command=True)
        if not cameras:  # pragma: no cover
            return

        if image_type == "bias":
            if exptime and exptime > 0:
                command.warning("setting exposure time for bias to 0 seconds.")
            exptime = 0.0

        if filename and len(cameras) > 1:
            return command.fail(
                "--filename can only be used when exposing a single camera."
            )

        report_exposure_state_partial = partial(report_exposure_state, command)

        command.actor.listener.register_callback(report_exposure_state_partial)
        jobs = []
        for camera in cameras:
            jobs.append(
                asyncio.create_task(
                    expose_one_camera(
                        command,
                        camera,
                        exptime,
                        image_type,
                        stack,
                        filename,
                        no_postprocess,
                        **exposure_kwargs,
                    )
                )
            )
        results = await asyncio.gather(*jobs)
        command.actor.listener.remove_callback(report_exposure_state_partial)

        if not all(results):
            return command.failed("one or more cameras failed to expose.")
        else:
            status = {}
            for camera in cameras:
                # Reset cameras to idle
                report_exposure_state(
                    command,
                    CameraEvent.EXPOSURE_IDLE,
                    {"name": camera.name},
                )
                status.update(
                    { 
                        camera.name:
                        {
                            "state": command.actor.exposure_state[camera.name].get("state", "NA"),
                            "filename": command.actor.exposure_state[camera.name].get("filename", "UNKNOWN"),
                        }
                    }
                )

            return command.finish(status)
        
    except Exception as ex:
        return command.error(error=ex)

