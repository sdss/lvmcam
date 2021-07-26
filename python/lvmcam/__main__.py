#!/usr/bin/env python
# encoding: utf-8
#
# @Author: José Sánchez-Gallego
# @Date: Dec 1, 2017
# @Filename: cli.py
# @License: BSD 3-Clause
# @Copyright: José Sánchez-Gallego

import sys
import os
import asyncio
.pyenv/versions/lvmagp-test/binimport click
from click_default_group import DefaultGroup
from clu.tools import cli_coro as cli_coro_lvm

from sdsstools.daemonizer import DaemonGroup

from lvmcam.actor.actor import lvmcam as lvmcamInstance

@click.group(cls=DefaultGroup, default="actor", default_if_no_args=True)
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the user configuration file.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Debug mode. Use additional v for more details.",
)
@click.pass_context
def lvmcam(ctx, config_file, verbose):
    """lvm controller"""

    ctx.obj = {"verbose": verbose, "config_file": config_file}


@lvmcam.group(cls=DaemonGroup, prog="lvmcam_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro_lvm
async def actor(ctx):
    """Runs the actor."""

    default_config_file = os.path.join(os.path.dirname(__file__), "etc/lvmcam.yml")
    config_file = ctx.obj["config_file"] or default_config_file

    lvmagp_obj = lvmagpInstance.from_config(config_file)
    if ctx.obj["verbose"]:
        lvmcam_obj.log.fh.setLevel(0)
        lvmcam_obj.log.sh.setLevel(0)
    await lvmcam_obj.start()
    await lvmcam_obj.run_forever()


if __name__ == "__main__":
    lvmcam()
