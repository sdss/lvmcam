from __future__ import annotations, print_function, division, absolute_import

import asyncio
import click
from clu.command import Command
from araviscam import BlackflyCam as blc

# from lvmieb.controller.controller import IebController
# from lvmieb.exceptions import LvmIebError

from . import parser

__all__ = ["singleframe"]


@parser.group()
def singleframe(*args):
    """test"""

    pass


@singleframe.command()
# @click.option(
#   "-s",
#   "--side",
#   type=click.Choice(["all", "right", "left"]),
#   default = "all",
#   help="all, right, or left",
# )
async def expose(command: Command):
    asyncio.run(blc.singleFrame(0.5,-1.0,False))
    command.info("Exposing")
