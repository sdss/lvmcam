# encoding: utf-8
#
# conftest.py

"""
Here you can add fixtures that will be used for all the tests in this
directory. You can also add conftest.py files in underlying subdirectories.
Those conftest.py will only be applies to the tests in that subdirectory and
underlying directories. See https://docs.pytest.org/en/2.7.3/plugins.html for
more information.
"""

import os

import clu.testing
# import numpy
import pytest
from clu.actor import AMQPBaseActor

from sdsstools import merge_config, read_yaml_file

from lvmcam import config
from lvmcam.actor import LvmcamActor


# import pathlib






@pytest.fixture()
def test_config():
    extra = read_yaml_file(os.path.join(os.path.dirname(__file__), "config.yaml"))
    yield merge_config(extra, config)


@pytest.fixture()
async def actor(test_config: dict, mocker):
    mocker.patch.object(AMQPBaseActor, "start")

    _actor = LvmcamActor.from_config(test_config)
    await _actor.start()

    _actor = await clu.testing.setup_test_actor(_actor)

    yield _actor

    _actor.mock_replies.clear()
    await _actor.stop()
