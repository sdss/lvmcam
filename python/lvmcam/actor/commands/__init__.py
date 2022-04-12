# /usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Changgon Kim, Taeeun Kim, Mingyeong YANG (mingyeong@khu.ac.kr), Sumin Lee(lxmark888@khu.ac.kr)
# @Date: 2021-07-14
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import glob
import importlib
import os

import click
#from basecam.actor.commands import camera_parser
from clu.parsers.click import CluGroup, help_, ping, version, get_schema
from cluplus.parsers.click import __commands

# we do create our own parser to remove the basecam caommands
@click.group(cls=CluGroup)
def camera_parser():
    pass


camera_parser.add_command(ping)
camera_parser.add_command(version)
camera_parser.add_command(help_)
camera_parser.add_command(__commands)
camera_parser.add_command(get_schema)

# Autoimport all modules in this directory so that they are added to the camera_parser.

exclusions = ["__init__.py"]

cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

files = [
    file_ for file_ in glob.glob("**/*.py", recursive=True) if file_ not in exclusions
]

for file_ in files:
    modname = file_[0:-3].replace("/", ".")
    mod = importlib.import_module(
        "lvmcam.actor.commands." + modname
    )  # changged by CK 2021/03/30

os.chdir(cwd)
_MIXIN_TO_COMMANDS = {
    "ShutterMixIn": [shutter],
    "CoolerMixIn": [temperature],
    "ImageAreaMixIn": [binning, area],
}
