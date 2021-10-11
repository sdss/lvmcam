import click
import pytest
from clu import JSONActor
from clu.testing import setup_test_actor

from lvmcam.actor.commands import parser as cam_command_parser


@pytest.mark.asyncio
async def test_actor():

    test_actor = await setup_test_actor(
        JSONActor("lvmcam", host="localhost", port=9999)
    )

    test_actor.parser = cam_command_parser

    await test_actor.start()

    command = test_actor.invoke_mock_command("connect -t")
    await command

    assert command.status.is_done

    reply2 = test_actor.mock_replies[-2]
    assert reply2["text"] == "{'name': test, 'uid': -1}"
