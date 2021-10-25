from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from clu.command import Command

from lvmcam.flir import FLIR_Utils as flir

from . import parser


__all__ = ["status"]


@parser.command()
@click.option("-v", "--verbose", type=bool, default=False)
async def status(command: Command, verbose):
    """
    Show status of camera

    Example
    -------

    .. code-block:: console

    $ clu
    lvmcam status
    12:14:48.884 lvmcam >
    12:14:51.161 lvmcam i {
        "STATUS": {
            "Camera model": "Blackfly S BFS-PGE-16S7M",
            "Camera vendor": "FLIR",
            "Camera id": "19283193",
            "Pixel format": "Mono16",
            "Available Formats": "['Mono8', 'Mono16', 'Mono10Packed', 'Mono12Packed', 'Mono10p', 'Mono12p']",
            "Full Frame": "1608x1104",
            "ROI": "1600x1100 at 0,0",
            "Frame size": "3520000 Bytes",
            "Frame rate": "27.695798215061195 Hz",
            "Exposure time": "0.099996 seconds",
            "Gain Conv.": "LCG",
            "Gamma Enable": "False",
            "Gamma Value": "0.800048828125",
            "Acquisition mode": "SingleFrame",
            "Framerate bounds": "(min=1.0, max=31.46968198249933)",
            "Exp. time bounds": "(min=14.0, max=30000003.0)",
            "Gain bounds": "(min=0.0, max=47.994294033026364)",
            "Power Supply Voltage": "9.76171875 V",
            "Power Supply Current": "0.259765625 A",
            "Total Dissiapted Power": "2.569320797920227 W",
            "Camera Temperature": "55.25 C"
        }
    }
    12:14:51.166 lvmcam :

    """
    try:
        cam, dev = flir.setup_camera(verbose)
        status = await flir.custom_status(cam, dev)
    except ValueError:
        command.error("There are not real cameras")

    command.info(STATUS=status)
    return command.finish()
