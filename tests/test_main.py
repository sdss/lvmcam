import pytest
from lvmcam.actor import LvmcamActor

pytestmark = [pytest.mark.asyncio]


async def test_actor(actor: LvmcamActor):

    command = await actor.invoke_mock_command("help")
    await command
    assert command.status.did_succeed

    command = await actor.invoke_mock_command("--help")
    await command
    assert command.status.did_succeed

    command = await actor.invoke_mock_command("ping")
    await command
    assert command.status.did_succeed

    command = await actor.invoke_mock_command("version")
    await command
    assert command.status.did_succeed

    await actor.invoke_mock_command("status -v")

    # Real camera
    # command = await actor.invoke_mock_command("show all -v ")
    # await command
    # assert command.status.did_succeed

    # await actor.invoke_mock_command("show connection")

    # command = await actor.invoke_mock_command("connect -v")
    # await command
    # assert command.status.did_succeed

    # command = await actor.invoke_mock_command("show connection")
    # await command
    # assert command.status.did_succeed
    # reply = actor.mock_replies[-2]
    # camname = reply["CONNECTED"]["name"]

    # command = await actor.invoke_mock_command(f"expose -v -t 0.1 1 {camname}")
    # await command
    # assert command.status.did_succeed

    # command = await actor.invoke_mock_command(
    #     f'expose -v -r "00h42m44s" -d "41d16m09s" -K 10 -f 1800 0.1 1 {camname}'
    # )
    # await command
    # assert command.status.did_succeed

    # await actor.invoke_mock_command("disconnect")

    # Test camera
    command = await actor.invoke_mock_command("show all")
    await command
    assert command.status.did_succeed

    await actor.invoke_mock_command("show connection")

    # command = await actor.invoke_mock_command("connect")
    # await command
    # assert command.status.did_succeed

    # command = await actor.invoke_mock_command("show connection")
    # await command
    # assert command.status.did_succeed
    # reply = actor.mock_replies[-2]
    # camname = reply["CONNECTED"]["name"]

    # command = await actor.invoke_mock_command(f"expose -t 0.1 1 {camname}")
    # await command
    # assert command.status.did_succeed

    # command = await actor.invoke_mock_command(
    #     f'expose -r "00h42m44s" -d "41d16m09s" -K 10 -f 1800 0.1 1 {camname}'
    # )
    # await command
    # assert command.status.did_succeed

    # command = await actor.invoke_mock_command("disconnect")
    # await command
    # assert command.status.did_succeed
