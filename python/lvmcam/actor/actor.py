#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-08-09
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import pathlib

from araviscam import BlackflyCamera, BlackflyCameraSystem
from basecam import ImageNamer
from basecam.actor import BaseCameraActor
from basecam.models import Extension, FITSModel, basic_header_model
from clu import AMQPActor
from sdsstools import read_yaml_file

from lvmcam import __version__
from lvmcam.actor.commands import camera_parser
from lvmcam.models import camera


CWD = pathlib.Path(__file__).parents[1]
BASE_CAMERA_PARAMS = read_yaml_file(CWD / "etc/lvm.camera_param.agcam.yml")


def mergedicts(a, b):
    for key in b:
        if isinstance(a.get(key), dict) or isinstance(b.get(key), dict):
            mergedicts(a.get(key, {}), b.get(key, {}))
        else:
            a[key] = b[key]
    return a


def get_camera_class(config: dict):
    """Returns a caamera class with the correct image namer and fits model."""

    dirname = config.get("dirname", ".")
    basename = config.get("basename", "{camera.name}-{num:04d}.fits")

    header_model = basic_header_model
    # header_model.append(CameraCards)
    # header_model.append(GenicamCards())
    # header_model.append(ScraperParamCards())
    # header_model.append(WcsCards())

    raw = Extension(
        data="raw",
        header_model=header_model,
        compressed="RICE_1",
        name="RAW",
    )

    class LVMCamera(BlackflyCamera):
        fits_model = FITSModel([raw])
        image_namer = ImageNamer(basename=basename, dirname=dirname)

    return LVMCamera


class LVMCamActor(BaseCameraActor, AMQPActor):
    """The LVMCam actor."""

    def __init__(self, *args, **kwargs):
        # Update camera config with default parameters.
        config = kwargs.get("config", {})

        for cam in config["cameras"]:
            camera_config = config["cameras"][cam]
            config["cameras"][cam] = mergedicts(camera_config, BASE_CAMERA_PARAMS)

        camera_class = get_camera_class(config)
        camera_system = BlackflyCameraSystem(camera_class, config["cameras"])

        super().__init__(camera_system, *args, **kwargs)
