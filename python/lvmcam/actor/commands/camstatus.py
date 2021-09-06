from __future__ import absolute_import, annotations, division, print_function

import asyncio

import click
# import gi  # To ensure correct Aravis version
from clu.command import Command

from . import parser


# gi.require_version('Aravis', '0.8')     # Version check
from gi.repository import Aravis  # Aravis package


__all__ = ["status"]


async def custom_status(cam, dev):
    [fullWidth, fullHeight] = cam.get_sensor_size()    # Full frame size
    [x, y, width, height] = cam.get_region()             # Get RoI details
    payload = cam.get_payload()                       # Get "payload", the size of in bytes

    stat = {
        "Camera vendor": f"{cam.get_vendor_name()}",
        "Camera model": f"{cam.get_model_name()}",
        "Camera id": f"{cam.get_device_id()}",
        "Pixel format": f"{cam.get_pixel_format_as_string()}",
        "Available Formats": f"{cam.dup_available_pixel_formats_as_display_names()}",
        "Full Frame": f"{fullWidth}x{fullHeight}",
        "ROI": f"{width}x{height} at {x},{y}",
        "Frame size": f"{payload} Bytes",
        "Frame rate": f"{cam.get_frame_rate()} Hz",
        "Exposure time": f"{cam.get_exposure_time()/1.0E6} seconds",
        "Gain Conv.": f"{cam.get_string('GainConversion')}",
        "Gamma Enable": f"{cam.get_boolean('GammaEnable')}",
        "Gamma Value": f"{cam.get_float('Gamma')}",
        "Acquisition mode": f"{Aravis.acquisition_mode_to_string(cam.get_acquisition_mode())}",
        "Framerate bounds": f"{cam.get_frame_rate_bounds()}",
        "Exp. time bounds": f"{cam.get_exposure_time_bounds()}",
        "Gain bounds": f"{cam.get_gain_bounds()}",
        "Power Supply Voltage": f"{cam.get_float('PowerSupplyVoltage')} V",
        "Power Supply Current": f"{cam.get_float('PowerSupplyCurrent')} A",
        "Total Dissiapted Power": f"{cam.get_float('PowerSupplyVoltage')*cam.get_float('PowerSupplyCurrent')} W",
        "Camera Temperature": f"{dev.get_float_feature_value('DeviceTemperature')} C"
    }
    return stat


def get_camera():
    Aravis.update_device_list()
    camera = Aravis.Camera.new(Aravis.get_device_id(0))
    device = camera.get_device()
    return camera, device


@parser.command()
@click.option('--verbose', type=bool, default=False)
async def status(command: Command, verbose):
    """
    Show status of camera
    """
    # print(Aravis.get_device_id(0))
    cam, dev = get_camera()
    # cam,dev = FLIR_Utils.Setup_Camera(verbose,False)
    # FLIR_Utils.Standard_Settings(cam,dev,verbose)
    command.info(status=await custom_status(cam, dev))
    return
