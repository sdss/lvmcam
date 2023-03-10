from basecam.actor.commands import camera_parser
from clu.command import Command


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
