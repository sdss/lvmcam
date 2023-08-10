#!/usr/bin/env python
# encoding: utf-8
#
# @Author: José Sánchez-Gallego
# @Date: Dec 1, 2017
# @Filename: cli.py
# @License: BSD 3-Clause
# @Copyright: José Sánchez-Gallego

import os

import click
from click_default_group import DefaultGroup

from clu.tools import cli_coro as cli_coro_lvm
from sdsstools import read_yaml_file
from sdsstools.daemonizer import DaemonGroup

from lvmcam.actor.actor import LVMCamActor


@click.group(cls=DefaultGroup, default="actor")
@click.argument(
    "CONFIG_FILE",
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "-r",
    "--rmq_url",
    "rmq_url",
    default=None,
    type=str,
    help="rabbitmq url, eg: amqp://guest:guest@localhost:5672/",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Debug mode. Use additional v for more details.",
)
@click.pass_context
def lvmcam(ctx, config_file: str, rmq_url: str | None = None, verbose: bool = False):
    """LVM AG camera actor."""

    ctx.obj = {
        "verbose": verbose,
        "config_file": config_file,
        "rmq_url": rmq_url,
    }


@lvmcam.group(cls=DaemonGroup, prog="lvmcam_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro_lvm
async def actor(ctx):
    """Runs the actor."""

    config_file = ctx.obj["config_file"]
    if not os.path.isabs(config_file):
        config_file = os.path.join(os.path.dirname(__file__), "etc", config_file)

    config = read_yaml_file(config_file)

    lvmcam_obj = LVMCamActor.from_config(
        config,
        url=ctx.obj["rmq_url"],
        verbose=ctx.obj["verbose"],
    )

    await lvmcam_obj.start()
    await lvmcam_obj.run_forever()


def main():
    lvmcam(auto_envvar_prefix="LVMCAM")


if __name__ == "__main__":
    main()
