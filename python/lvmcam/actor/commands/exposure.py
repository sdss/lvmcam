#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio
import json

import click

# from lvmscp.exceptions import lvmscpError

from . import parser


# lock for exposure lock
exposure_lock = asyncio.Lock()


@parser.command()
@click.argument("COUNT", type=int, default=1, required=False)
@click.argument(
    "FLAVOUR",
    type=click.Choice(["bias", "object", "flat", "dark"]),
    default="object",
    required=False,
)
@click.argument("EXPTIME", type=float, required=False)
@click.argument(
    "spectro",
    type=click.Choice(["sp1", "sp2", "sp3"]),
    default="sp1",
    required=False,
)
async def exposure(command, exptime: float, count: int, flavour: str, spectro: str):
    """Exposure command controlling all lower actors"""

    # Check the exposure time input (bias = 0.0)
    if flavour != "bias" and exptime is None:
        raise click.UsageError("EXPOSURE-TIME is required unless --flavour=bias.")
    elif flavour == "bias":
        exptime = 0.0

    if exptime < 0.0:
        raise click.UsageError("EXPOSURE-TIME cannot be negative")

    # lock for exposure sequence only running for one delegate
    async with exposure_lock:

        command.info(text="Pinging . . .")
        err = await check_actor_ping(command, "lvmnps")
        if err is True:
            command.info(text="lvmnps OK!")
            pass
        else:
            return command.fail(text=err)

        err = await check_actor_ping(command, "archon")
        if err is True:
            command.info(text="archon OK!")
            pass
        else:
            return command.fail(text=err)

        err = await check_actor_ping(command, "lvmieb")
        if err is True:
            command.info(text="lvmieb OK!")
            pass
        else:
            return command.fail(text=err)

        command.info(text="Checking device Power . . .")
        err = await check_device_power(command, spectro)
        if err is True:
            command.info(text="device power OK!")
            pass
        else:
            return command.fail(text=err)

        command.info(text="Checking Shutter Closed . . .")
        err = await check_shutter_closed(command, spectro)
        if err is True:
            command.info(text="Shutter Closed!")
            pass
        else:
            return command.fail(text=err)

        if flavour == "object" or flavour == "flat":
            command.info(text="Checking hartmann opened")
            err = await check_hartmann_opened(command, spectro)
            if err is True:
                pass
            else:
                return command.fail(text=err)

        command.info(text="Checking archon controller initialized . . .")
        err = await check_archon(command, spectro)
        if err is True:
            command.info(text="archon initialized!")
            pass
        else:
            return command.fail(text=err)

        if flavour == "flat":
            command.info(text="Checking flat lamps . . .")
            err = await check_flat_lamp(command)
            if err is True:
                command.info(text="flat lamps on!")
                pass
            else:
                return command.fail(text=err)

        command.info(text="Starting the exposure.")
        # start exposure loop
        for nn in range(count):

            command.info(f"Taking exposure {nn + 1} of {count}.")

            header_json = await extra_header_telemetry(command, spectro)

            # Flushing before CCD exposure
            flush_count = 1
            if flush_count > 0:
                command.info("Flushing")
                archon_cmd = await (
                    await command.actor.send_command(
                        "archon", f"flush {flush_count} {spectro}"
                    )
                )
                if archon_cmd.status.did_fail:
                    return command.fail(text="Failed flushing")

            # Start CCD exposure
            archon_cmd = await (
                await command.actor.send_command(
                    "archon",
                    f"expose start {spectro} --{flavour} {exptime}",
                )
            )
            if archon_cmd.status.did_fail:
                await command.actor.send_command("archon", "expose abort --flush")
                return command.fail(
                    text="Failed starting exposure. Trying to abort and exiting."
                )
            else:
                reply = archon_cmd.replies
                command.info(text=reply[-2].body["text"])

            if (flavour != "bias" and flavour != "dark") and exptime > 0:
                # Use command to access the actor and command the shutter

                command.info("Opening the shutter")

                shutter_cmd = await command.actor.send_command(
                    "lvmieb", f"shutter open {spectro}"
                )
                await shutter_cmd

                if shutter_cmd.status.did_fail:
                    await command.actor.send_command(
                        "lvmieb", f"shutter close {spectro}"
                    )
                    await command.actor.send_command("archon", "expose abort --flush")
                    return command.fail(text="Shutter failed to open")

                # Report status of the shutter
                replies = shutter_cmd.replies
                shutter_status = replies[-1].body["shutter"]
                if shutter_status not in ["opened", "closed"]:
                    return command.fail(
                        text=f"Unknown shutter status {shutter_status!r}."
                    )

                command.info(f"Shutter is now {shutter_status!r}.")

                if not (
                    await asyncio.create_task(
                        close_shutter_after(command, exptime, spectro)
                    )
                ):
                    await command.actor.send_command("archon", "expose abort --flush")
                    return command.fail(text="Failed to close the shutter")

            # Readout pending information
            command.info(text="readout . . .")

            # Finish exposure
            archon_cmd = await (
                await command.actor.send_command(
                    "archon",
                    "expose finish",
                    f"--header '{header_json}'",
                )
            )

            replies = archon_cmd.replies

            if archon_cmd.status.did_fail:
                command.info(replies[-1].body)
                command.fail(text="Failed reading out exposure")
            else:
                # For monitering the status
                while True:
                    readout_cmd = await command.actor.send_command(
                        "archon", f"status {spectro}"
                    )
                    await readout_cmd
                    readout_replies = readout_cmd.replies
                    archon_readout = readout_replies[-2].body["status"]["status_names"][
                        0
                    ]
                    if archon_readout == "READING":
                        continue
                    else:
                        command.info(text="readout finished!")
                        break

                command.info(replies[-8].body)
                command.info(replies[-7].body)
                command.info(replies[-6].body)
                command.info(replies[-5].body)
                command.info(replies[-4].body)
                command.info(replies[-3].body)
                command.info(replies[-2].body)

        return command.finish(text="Exposure sequence done!")


async def close_shutter_after(command, delay: float, spectro: str):
    """Waits ``delay`` before closing the shutter."""

    command.info(text="exposing . . .")
    await asyncio.sleep(delay)

    command.info(text="Closing the shutter")
    shutter_cmd = await command.actor.send_command("lvmieb", f"shutter close {spectro}")
    await shutter_cmd

    if shutter_cmd.status.did_fail:
        command.fail(text="Shutter failed to close.")
        return False

    replies = shutter_cmd.replies
    shutter_status = replies[-1].body["shutter"]
    if shutter_status not in ["opened", "closed"]:
        return command.fail(text=f"Unknown shutter status {shutter_status!r}.")

    command.info(text=f"Shutter is now '{shutter_status}'")
    return True


async def check_actor_ping(command, actor_name):

    # Check the actor is running
    try:
        status_cmd = await command.actor.send_command(actor_name, "ping")
        await status_cmd
    except lvmscpError as err:
        return str(err)

    if status_cmd.status.did_fail:
        return status_cmd.status
    else:
        return True


async def check_device_power(command, spectro: str):

    # check the power of the shutter & hartmann doors
    wago_power_status_cmd = await command.actor.send_command(
        "lvmieb", f"wago getpower {spectro}"
    )
    await wago_power_status_cmd

    if wago_power_status_cmd.status.did_fail:
        return "Failed to receive the power status from wago relays"
    else:
        replies = wago_power_status_cmd.replies
        shutter_power_status = replies[-1].body["shutter_power"]
        hartmann_left_power_status = replies[-1].body["hartmann_left_power"]
        hartmann_right_power_status = replies[-1].body["hartmann_right_power"]

        if shutter_power_status == "OFF":
            return "Cannot start exposure : Exposure shutter power off"
        elif hartmann_left_power_status == "OFF":
            return "Cannot start exposure : Left hartmann door power off"
        elif hartmann_right_power_status == "OFF":
            return "Cannot start exposure : Right hartmann door power off"
        else:
            return True


async def check_shutter_closed(command, spectro: str):
    """Check the open/closed status of the shutter"""
    shutter_status_cmd = await command.actor.send_command(
        "lvmieb", f"shutter status {spectro}"
    )
    await shutter_status_cmd

    if shutter_status_cmd.status.did_fail:
        return "Failed to receive the status of the shutter status"
    else:
        replies = shutter_status_cmd.replies
        shutter_status_before = replies[-1].body["shutter"]

        if shutter_status_before != "closed":
            return "Shutter is already opened. The command will fail"
        else:
            return True


async def check_hartmann_opened(command, spectro: str):
    # Check the status (opened / closed) of the hartmann doors
    hartmann_status_cmd = await command.actor.send_command(
        "lvmieb", f"hartmann status {spectro}"
    )
    await hartmann_status_cmd

    if hartmann_status_cmd.status.did_fail:
        return "Failed to receive the status of the hartmann status"
    else:
        replies = hartmann_status_cmd.replies
        hartmann_left_status = replies[-1].body["hartmann_left"]
        hartmann_right_status = replies[-1].body["hartmann_right"]

        if not (hartmann_left_status == "opened" and hartmann_right_status == "opened"):
            return "Hartmann doors are not opened for the science exposure"
        else:
            return True


async def check_archon(command, spectro: str):
    """Check the archon CCD status"""
    # Check that the configuration of archon controller has been loaded.
    archon_cmd = await (await command.actor.send_command("archon", f"status {spectro}"))
    if archon_cmd.status.did_fail:
        return "Failed getting status from the controller"
    else:
        replies = archon_cmd.replies
        check_idle = replies[-2].body["status"]["status_names"][0]
        if check_idle != "IDLE":
            return "archon is not initialized"
        else:
            return True


async def check_flat_lamp(command):
    """Check the flat lamp status"""
    flat_lamp_cmd = await (
        await command.actor.send_command("lvmnps", "status what Krypton")
    )
    if flat_lamp_cmd.status.did_fail:
        return "Failed getting status from the network power switch"
    else:
        replies = flat_lamp_cmd.replies
        check_lamp = replies[-2].body["STATUS"]["DLI-NPS-03"]["Krypton"]["STATE"]
        if check_lamp:
            command.info(text="flat lamp is on!")
            return True
        else:
            return "flat lamp is off..."


async def extra_header_telemetry(command, spectro: str):
    """telemetry from the devices and add it on the header"""
    # Build extra header.
    scp_status_cmd = await command.actor.send_command("lvmscp", f"status {spectro}")
    await scp_status_cmd

    if scp_status_cmd.status.did_fail:
        return "Failed to receive the status of the lvmscp"
    else:
        replies = scp_status_cmd.replies
        rhtRH1 = replies[-2].body["IEB_HUMIDITY"]["rhtRH1"]
        rhtRH2 = replies[-2].body["IEB_HUMIDITY"]["rhtRH2"]
        rhtRH3 = replies[-2].body["IEB_HUMIDITY"]["rhtRH3"]
        rhtT1 = replies[-2].body["IEB_TEMPERATURE"]["rhtT1"]
        rhtT2 = replies[-2].body["IEB_TEMPERATURE"]["rhtT2"]
        rhtT3 = replies[-2].body["IEB_TEMPERATURE"]["rhtT3"]
        rtd1 = replies[-2].body["IEB_TEMPERATURE"]["rtd1"]
        rtd2 = replies[-2].body["IEB_TEMPERATURE"]["rtd2"]
        rtd3 = replies[-2].body["IEB_TEMPERATURE"]["rtd3"]
        rtd4 = replies[-2].body["IEB_TEMPERATURE"]["rtd4"]

        if replies[-2].body["NETWORK_POWER_SWITCHES"]["STATUS"]["DLI-NPS-02"][
            "LN2 NIR valve"
        ]["STATE"]:
            ln2_nir = "ON"
        else:
            ln2_nir = "OFF"

        if replies[-2].body["NETWORK_POWER_SWITCHES"]["STATUS"]["DLI-NPS-02"][
            "LN2 Red Valve"
        ]["STATE"]:
            ln2_red = "ON"
        else:
            ln2_red = "OFF"

        header_dict = {
            "rhtRH1": (rhtRH1, "IEB rht sensor humidity [%]"),
            "rhtRH2": (rhtRH2, "IEB rht sensor humidity [%]"),
            "rhtRH3": (rhtRH3, "IEB rht sensor humidity [%]"),
            "rhtT1": (rhtT1, "IEB rht sensor Temperature [C]"),
            "rhtT2": (rhtT2, "IEB rht sensor Temperature [C]"),
            "rhtT3": (rhtT3, "IEB rht sensor Temperature [C]"),
            "rtd1": (rtd1, "IEB rtd sensor Temperature [C]"),
            "rtd2": (rtd2, "IEB rtd sensor Temperature [C]"),
            "rtd3": (rtd3, "IEB rtd sensor Temperature [C]"),
            "rtd4": (rtd4, "IEB rtd sensor Temperature [C]"),
            "LN2NIR": (
                ln2_nir,
                replies[-2].body["NETWORK_POWER_SWITCHES"]["STATUS"]["DLI-NPS-02"][
                    "LN2 NIR valve"
                ]["DESCR"],
            ),
            "LN2RED": (
                ln2_red,
                replies[-2].body["NETWORK_POWER_SWITCHES"]["STATUS"]["DLI-NPS-02"][
                    "LN2 Red Valve"
                ]["DESCR"],
            ),
        }

        header_json = json.dumps(header_dict, indent=None)
        return header_json