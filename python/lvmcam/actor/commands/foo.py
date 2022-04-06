import asyncio

import click
from clu.command import Command
from basecam.actor.commands import camera_parser


__all__ = ["foo"]

@camera_parser.command(name="foo")
async def foo(command: Command):
    """
    Foo !
    """
    try:
        return command.finish(text="foo")
        
    except ValueError as ex:
        return command.fail(error=ex)
        



