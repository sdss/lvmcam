from lvmcam.araviscam.aravis import Aravis
from lvmcam.actor import modules
import basecam.models.card as card
# from lvmcam.actor.commands import connection

# --------------------------------------------------------------------------------------------


class CamCards(card.MacroCard):
    def macro(self, exposure, context={}):
        camname = modules.variables.camname
        # print(camname)

        cam, dev, _ = modules.variables.Aravis_available_camera[camname]
        [fullWidth, fullHeight] = cam.get_sensor_size()  # Full frame size
        [x, y, width, height] = cam.get_region()  # Get RoI details
        payload = cam.get_payload()  # Get "payload", the size of in bytes

        status = [('PXFORMAT', cam.get_pixel_format_as_string(), "Pixel format"),
                  ('FULLFRAM', f"{fullWidth}x{fullHeight}", "Full Frame"),
                  ("ROI", f"{width}x{height} at {x},{y}", "ROI"),
                  ("FRAMSIZE", payload, "Frame size (Bytes)"),
                  ("FRAMRATE", cam.get_frame_rate(), "Frame rate (Hz)"),
                  ("EXPTIME", cam.get_exposure_time() / 1.0E6, "Exposure time (seconds)"),
                  ("GAINCONV", cam.get_string('GainConversion'), "Gain Conv."),
                  ("GAMMAENA", cam.get_boolean('GammaEnable'), "Gamma Enable"),
                  ("GAMMAVAL", cam.get_float('Gamma'), "Gamma Value"),
                  ("ACQUIMOD", Aravis.acquisition_mode_to_string(cam.get_acquisition_mode()), "Acquisition mode"),
                  ("FRMRATBD", str(cam.get_frame_rate_bounds()), "Framerate bounds"),
                  ("EXPTIMBD", str(cam.get_exposure_time_bounds()), "Exp. time bounds"),
                  ("GAINBD", str(cam.get_gain_bounds()), "Gain bounds"),
                  ("VOLTAGE", cam.get_float('PowerSupplyVoltage'), "Power Supply Voltage (V)"),
                  ("CURRENT", cam.get_float('PowerSupplyCurrent'), "Power Supply Current (A)"),
                  ("POWER", cam.get_float('PowerSupplyVoltage') * cam.get_float('PowerSupplyCurrent'), "Total Dissiapted Power (W)"),
                  ("CAMTEMP", dev.get_float_feature_value('DeviceTemperature'), "Camera Temperature (C)")]

        return status

# --------------------------------------------------------------------------------------------


async def custom_status(cam, dev):
    [fullWidth, fullHeight] = cam.get_sensor_size()  # Full frame size
    [x, y, width, height] = cam.get_region()  # Get RoI details
    payload = cam.get_payload()  # Get "payload", the size of in bytes

    stat = {
        "Camera id": f"{cam.get_device_id()}",
        "Camera model": f"{cam.get_model_name()}",
        "Camera vendor": f"{cam.get_vendor_name()}",
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
        "Camera Temperature": f"{dev.get_float_feature_value('DeviceTemperature')} C",
    }
    return stat


# # --------------------------------------------------------------------------------------------


# async def status_for_header(cam):
#     # [fullWidth, fullHeight] = cam.get_sensor_size()  # Full frame size
#     [x, y, width, height] = cam.get_region()  # Get RoI details
#     # payload = cam.get_payload()  # Get "payload", the size of in bytes

#     stat = {
#         "Pixel format": f"{cam.get_pixel_format_as_string()}",
#         "Available Formats": f"{cam.dup_available_pixel_formats_as_display_names()}",
#         "ROI": f"{width}x{height} at {x},{y}",
#         "Frame rate": f"{cam.get_frame_rate()} Hz",
#         "Gain Conv.": f"{cam.get_string('GainConversion')}",
#         "Gamma Enable": f"{cam.get_boolean('GammaEnable')}",
#         "Gamma Value": f"{cam.get_float('Gamma')}",
#         "Acquisition mode": f"{Aravis.acquisition_mode_to_string(cam.get_acquisition_mode())}",
#         "Framerate bounds": f"{cam.get_frame_rate_bounds()}",
#         "Exp. time bounds": f"{cam.get_exposure_time_bounds()}",
#         "Gain bounds": f"{cam.get_gain_bounds()}",
#     }
#     return stat


# async def vol_cur_tem(cam, dev):
#     # [fullWidth, fullHeight] = cam.get_sensor_size()  # Full frame size
#     # [x, y, width, height] = cam.get_region()  # Get RoI details
#     # payload = cam.get_payload()  # Get "payload", the size of in bytes

#     stat = {
#         # "Pixel format": f"{cam.get_pixel_format_as_string()}",
#         # "Available Formats": f"{cam.dup_available_pixel_formats_as_display_names()}",
#         # "ROI": f"{width}x{height} at {x},{y}",
#         # "Frame rate": f"{cam.get_frame_rate()} Hz",
#         # "Gain Conv.": f"{cam.get_string('GainConversion')}",
#         # "Gamma Enable": f"{cam.get_boolean('GammaEnable')}",
#         # "Gamma Value": f"{cam.get_float('Gamma')}",
#         # "Acquisition mode": f"{Aravis.acquisition_mode_to_string(cam.get_acquisition_mode())}",
#         # "Framerate bounds": f"{cam.get_frame_rate_bounds()}",
#         # "Exp. time bounds": f"{cam.get_exposure_time_bounds()}",
#         # "Gain bounds": f"{cam.get_gain_bounds()}",
#         "Power Supply Voltage": f"{cam.get_float('PowerSupplyVoltage')} V",
#         "Power Supply Current": f"{cam.get_float('PowerSupplyCurrent')} A",
#         # "Total Dissiapted Power": f"{cam.get_float('PowerSupplyVoltage')*cam.get_float('PowerSupplyCurrent')} W",
#         "Camera Temperature": f"{dev.get_float_feature_value('DeviceTemperature')} C",
#     }
#     return stat


# --------------------------------------------------------------------------------------------


# def setup_camera():
#     Aravis.update_device_list()
#     try:
#         cam = Aravis.Camera.new(Aravis.get_device_id(0))
#     except:
#         print("ERROR - No camera found")
#         return None, None
#     dev = cam.get_device()
#     return cam, dev


def setup_camera():
    Aravis.update_device_list()
    Ndev = Aravis.get_n_devices()
    for i in range(Ndev):
        cam = Aravis.Camera.new(Aravis.get_device_id(i))
        dev = cam.get_device()
        uid = cam.get_string("DeviceSerialNumber")
        modules.variables.Aravis_available_camera[i] = (cam, dev, uid)


# def setup_camera(verbose, fakeCam=False):

#     """
#     Instantiates a camera and returns it, along with the corresponding "dev". This
#     gives access to "deeper" camera functions, such as the device temperature.

#     If fakeCam = True, it returns the fake camera object, a software equivalent,
#     with (presumably realistic) noise, etc.

#     """

#     Aravis.update_device_list()  # Scan for live cameras

#     if fakeCam:
#         Aravis.enable_interface("Fake")  # using arv-fake-gv-camera-0.8
#         cam = Aravis.Camera.new(None)  # Instantiate cam

#         if verbose:
#             print("Instantiated FakeCam")

#     else:  # Note: We expect only one "real" camera !!

#         try:
#             cam = Aravis.Camera.new(Aravis.get_device_id(0))  # Instantiate cam
#             # if verbose:
#             #     print(f"[DEBUG]: [{__name__}]: Instantiated real camera")
#         except:
#             print("ERROR - No camera found")  # Ooops!!
#             return None, None, None  # Send back nothing

#     dev = cam.get_device()  # Allows access to "deeper" features

#     return cam, dev  # Send back camera, device
