# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel(briegel@mpia.de)
# @Date: 2022-04-06
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import glob
import importlib
import os

import click

from clu.command import Command
from clu.parsers.click import CluGroup, command_parser, get_schema, help_, ping, version
from cluplus.parsers.click import __commands


@click.group(cls=CluGroup)
def parser(*args):
    pass


parser.add_command(ping)
parser.add_command(version)
parser.add_command(help_)
parser.add_command(get_schema)
parser.add_command(__commands)


# Autoimport all modules in this directory so that they are added to the parser.

exclusions = ["__init__.py"]

cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

files = [
    file_ for file_ in glob.glob("**/*.py", recursive=True) if file_ not in exclusions
]

print(files)

for file_ in files:
    modname = file_[0:-3].replace("/", ".")
    mod = importlib.import_module(
        "lvmtel.actor.commands." + modname
    )  # changged by CK 2021/03/30

os.chdir(cwd)
