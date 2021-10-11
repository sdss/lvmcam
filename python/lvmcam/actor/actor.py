from __future__ import absolute_import, annotations, division, print_function

from clu.actor import AMQPActor

from lvmcam.actor.commands import parser as lvm_command_parser


# import asyncio
# import os
# import warnings
# from contextlib import suppress


# from scpactor import __version__

__all__ = ["lvmcam"]


class lvmcam(AMQPActor):
    """agp controller actor."""

    parser = lvm_command_parser

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
