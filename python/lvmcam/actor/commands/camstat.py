from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
from clu.command import Command

from lvmcam.flir import (read_FLIR)  # auto run when actor started (30/07/21 Sumin)
from lvmcam.flir import FLIR_FullStatus, ResetFLIR, FLIR_Utils

from . import parser


#from lvmieb.controller.controller import IebController
#from lvmieb.exceptions import LvmIebError

__all__ = ["camstat"]


# currently not working due to problem of flir_utils
@parser.group()
def camstat(*args):
    """[TEST]control status of FLIR camera"""
    pass


@camstat.command()
# @click.option(
#    "-s",
#    "--side",
#    type=click.Choice(["all", "right", "left"]),
#    default = "all",
#    help="all, right, or left",
# )
async def readstat(command: Command):
    read_FLIR.readflir()
    command.info("test image and status of FLIR camera")


@camstat.command()
async def reset(command: Command):
    ResetFLIR.resetcam()
    command.info("FLIR reset")


@camstat.command()
async def fullstat(command: Command):
    FLIR_FullStatus.fullstat()
    command.info("full status of FLIR camera")


@camstat.command()
async def acquire(command: Command):
    camt, devt = FLIR_Utils.Setup_Camera(False)
    command.info(str(FLIR_Utils.Acquire_Frames(cam=camt, nFrames=1)))
    command.info("exposing single frame for test")


import gi  # To ensure correct Aravis version
gi.require_version('Aravis', '0.8')     # Version check
from gi.repository import Aravis  # Aravis package
async def custom_status(command, cam, dev):
    [fullWidth,fullHeight] = cam.get_sensor_size()    # Full frame size
    [x,y,width,height] = cam.get_region()             # Get RoI details
    payload = cam.get_payload()                       # Get "payload", the size of in bytes

    command.info(Camera_vendor=f"{cam.get_vendor_name()}")
    command.info(Camera_model=f"{cam.get_model_name()}")
    command.info(Camera_id=f"{cam.get_device_id()}")

    command.info(Pixel_format=f"{cam.get_pixel_format_as_string()}")
    command.info(Available_Formats=f"{cam.dup_available_pixel_formats_as_display_names()}")

    command.info(Full_Frame=f"{fullWidth}x{fullHeight}")
    command.info(ROI=f"{width}x{height} at {x},{y}")
    command.info(Frame_size=f"{payload} Bytes")

    command.info(Frame_rate=f"{cam.get_frame_rate()} Hz")
    command.info(Exposure_time=f"{cam.get_exposure_time()/1.0E6} seconds")
    command.info(Gain_Conversion=f"{cam.get_string('GainConversion')}")
    command.info(Gamma_enable=f"{cam.get_boolean('GammaEnable')}")
    command.info(Gamma_value=f"{cam.get_float('Gamma')}")

    command.info(Acquisition_mode=f"{Aravis.acquisition_mode_to_string(cam.get_acquisition_mode())}")
    command.info(Framerate_bounds=f"{cam.get_frame_rate_bounds()}")
    command.info(Exptime_bounds=f"{cam.get_exposure_time_bounds()}")
    command.info(Gain_bounds=f"{cam.get_gain_bounds()}")
    
    command.info(Power_Supply_Voltage=f"{cam.get_float('PowerSupplyVoltage')} V")
    command.info(Power_Supply_Current=f"{cam.get_float('PowerSupplyCurrent')} A")
    command.info(Total_Dissiapted_Power=f"{cam.get_float('PowerSupplyVoltage')*cam.get_float('PowerSupplyCurrent')} W")
    command.info(Camera_Temperature=f"{dev.get_float_feature_value('DeviceTemperature')} C")


@camstat.command()
@click.option('--verbose', type=bool, default=False)
async def status(command: Command, verbose):
    """
    Show status of camera
    """
    cam,dev = FLIR_Utils.Setup_Camera(verbose,False)    
    # FLIR_Utils.Standard_Settings(cam,dev,verbose) 
    await custom_status(command,cam,dev)
    return
