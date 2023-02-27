#!/usr/bin/env python
# encoding: utf-8
#
# @Author: José Sánchez-Gallego
# @Date: Dec 1, 2017
# @Filename: cli.py
# @License: BSD 3-Clause
# @Copyright: José Sánchez-Gallego

import asyncio
import os
import sys
from logging import DEBUG

import click
from click_default_group import DefaultGroup
from clu.tools import cli_coro as cli_coro_lvm
from lvmtel.actor.actor import LvmtelActor

from sdsstools import get_logger, read_yaml_file
from sdsstools.daemonizer import DaemonGroup
from sdsstools.logger import SDSSLogger, StreamFormatter


@click.group(cls=DefaultGroup, default="actor")
@click.option(
    "-c",
    "--config",
    "config_file",
    type=str,
    help="Path to the user configuration file.",
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
@click.option(
    "-s",
    "--simulate",
    count=True,
    help="Simulation mode.",
)
@click.pass_context
def lvmtel(ctx, config_file, rmq_url, verbose, simulate):
    """lvm controller"""

    ctx.obj = {
        "verbose": verbose,
        "config_file": config_file,
        "rmq_url": rmq_url,
        "simulate": simulate,
    }


@lvmtel.group(cls=DaemonGroup, prog="lvmtel_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro_lvm
async def actor(ctx):
    """Runs the actor."""

    config_file = ctx.obj["config_file"]
    lvmtel_obj = LvmtelActor.from_config(
        config_file,
        url=ctx.obj["rmq_url"],
        verbose=ctx.obj["verbose"],
        simulate=ctx.obj["simulate"],
    )

    await lvmtel_obj.start()
    await lvmtel_obj.run_forever()


if __name__ == "__main__":
    lvmtel()
