#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-08-09
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from basecam.actor.commands import camera_parser

from .gain import gain
from .reconnect import reconnect


camera_parser.commands["reconnect"] = reconnect
