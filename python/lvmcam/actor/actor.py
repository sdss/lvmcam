from __future__ import absolute_import, annotations, division, print_function

# from clu.actor import AMQPActor

# from lvmcam.actor.commands import parser as lvmcam_command_parser


# import asyncio
# import os
# import warnings
# from contextlib import suppress


# from scpactor import __version__

# import asyncio
import os

# import warnings
# from contextlib import suppress

# from typing import ClassVar, Dict, Type

# import click
# from clu.actor import AMQPActor, BaseActor

from lvmcam import __version__

# from lvmcam.exceptions import LvmcamUserWarning
from basecam.actor.commands import camera_parser as parser

__all__ = ["LvmcamBaseActor", "LvmcamActor"]

from clu import AMQPActor
from basecam.actor import BaseCameraActor

# from lvmcam.araviscam import BlackflyCam as blc
# from skymakercam.camera import SkymakerCameraSystem, SkymakerCamera
import sys
from sdsstools import read_yaml_file

from lvmcam.actor import modules

from lvmcam.araviscam import BlackflyCameraSystem, BlackflyCamera
from lvmcam.skymakercam import SkyCameraSystem, SkyCamera
camera_types = {"araviscam": lambda: BlackflyCameraSystem(BlackflyCamera),
                "skymakercam": lambda: SkyCameraSystem(SkyCamera)}

config = os.path.dirname(__file__)[:-6] + "/etc/camtype.yaml"
config = read_yaml_file(config)
camtype = config["camtype"]

is_True_gt_1 = sum(value is True for value in camtype.values()) > 1
if is_True_gt_1:
    print("The number of True in camtype.yaml is greater than 1")
    print("Only one True is allowed")
    sys.exit()

for item in camtype.items():
    if item[1] is True:
        modules.variables.camtypename = item[0]


class LvmcamBaseActor(BaseCameraActor):
    """Lvmcam base actor."""

    parser = parser

    def __init__(
        self,
        *args,
        **kwargs,
    ):

        if "schema" not in kwargs:
            kwargs["schema"] = os.path.join(
                os.path.dirname(__file__),
                "../etc/schema.json",
            )

        super().__init__(camera_types[modules.variables.camtypename](), *args, **kwargs)
        self.version = __version__


class LvmcamActor(LvmcamBaseActor, AMQPActor):
    """Lvmcam actor based on the AMQP protocol."""

    pass


# class LvmcamActor(AMQPActor):
#     """agp controller actor."""

#     parser = lvmcam_command_parser

#     def __init__(
#         self,
#         *args,
#         **kwargs,
#     ):
#         super().__init__(*args, **kwargs)
