import pytest
from lvmcam.actor import LvmcamActor

pytestmark = [pytest.mark.asyncio]


async def test_actor(actor: LvmcamActor):

    # command = await actor.invoke_mock_command("connect -t")
    # await command
    # assert command.status.did_succeed

    await actor.invoke_mock_command("help")
    await actor.invoke_mock_command("--help")
    await actor.invoke_mock_command("ping")
    await actor.invoke_mock_command("version")

    await actor.invoke_mock_command("status")

    await actor.invoke_mock_command("show all")
    await actor.invoke_mock_command("show connection")

    await actor.invoke_mock_command("connect")

    await actor.invoke_mock_command("show connection")
    await actor.invoke_mock_command("disconnect")
    await actor.invoke_mock_command("show connection")

    await actor.invoke_mock_command("connect -t")

    await actor.invoke_mock_command("expose 0.1 3 test")
    await actor.invoke_mock_command("expose -t 0.1 3 test")
    await actor.invoke_mock_command("expose -r 10 -d 10 -K 10 0.1 3 test")
    await actor.invoke_mock_command('expose -f "foo/bar" 0.1 3  test')
    await actor.invoke_mock_command("expose 0.2 1 test")

    await actor.invoke_mock_command("show connection")
    await actor.invoke_mock_command("disconnect")
    await actor.invoke_mock_command("show connection")
