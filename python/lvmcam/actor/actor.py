
from __future__ import annotations, print_function, division, absolute_import

import asyncio
import os
import warnings
from contextlib import suppress

from clu.actor import AMQPActor

#from scpactor import __version__


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

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)