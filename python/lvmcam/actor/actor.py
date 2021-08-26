
from __future__ import absolute_import, annotations, division, print_function

# import asyncio
# import os
# import warnings
# from contextlib import suppress

from clu.actor import AMQPActor

from lvmcam.actor.commands import parser as lvm_command_parser


# from scpactor import __version__

__all__ = ["lvmcam"]


class lvmcam(AMQPActor):
    """agp controller actor.
    In addition to the normal arguments and keyword parameters for
    `~clu.actor.AMQPActor`, the class accepts the following parameters.
    Parameters
    ----------
    controllers
        The list of `.agp_Controller` instances to manage.
    """
    parser = lvm_command_parser

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
