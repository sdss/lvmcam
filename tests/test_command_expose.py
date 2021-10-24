import pytest
from lvmcam.actor import lvmcam

pytestmark = [pytest.mark.asyncio]

async def test_connect_testcam(actor: lvmcam):

    command = await actor.invoke_mock_command("connect -t")
    await command

    assert command.status.did_succeed

    reply = actor.mock_replies[-2]
    assert reply["text"] == "{'name': test, 'uid': -1}"