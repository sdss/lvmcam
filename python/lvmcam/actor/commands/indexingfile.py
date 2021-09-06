from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from click.decorators import command
from clu.command import Command

from lvmcam.actor.commands import parser


__all__ = ["curindex"]


@parser.command()
async def curindex(
    command: Command,
):
    with open('file.txt', 'w+') as f:
        line = f.readline()
        print(line)
        command.info(line)
