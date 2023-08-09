import pytest
from lvmcam.actor import LvmcamActor


pytestmark = [pytest.mark.asyncio]


async def test_actor(actor: LvmcamActor):
    command = await actor.invoke_mock_command("--help")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail

    command = await actor.invoke_mock_command("ping")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail

    command = await actor.invoke_mock_command("version")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail

    command = await actor.invoke_mock_command("status")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail
        reply = actor.mock_replies
        assert reply[-2]["error"] == "There are not real cameras"

    command = await actor.invoke_mock_command("show all -v")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
        reply = actor.mock_replies
        assert isinstance(reply[-1]["ALL"], dict)
    elif command.status.did_fail:
        assert command.status.did_fail

    command = await actor.invoke_mock_command("show connection")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail
        reply = actor.mock_replies
        assert reply[-2]["error"] == "There are no connected cameras"

    command = await actor.invoke_mock_command("disconnect")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail
        reply = actor.mock_replies
        assert reply[-2]["error"] == "There is nothing to remove"

    command = await actor.invoke_mock_command("connect -v")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
        command = await actor.invoke_mock_command("connect")
        assert command.status.did_fail
    elif command.status.did_fail:
        assert command.status.did_fail

    command = await actor.invoke_mock_command("show connection")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail

    command = await actor.invoke_mock_command("expose -v -t 0.1 1 sci.agw")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail

    command = await actor.invoke_mock_command(
        "expose -v -r 00h42m44s -d 41d16m09s -K 10 -f 1800 -c NO 0.1 1 sci.agw"
    )
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail

    command = await actor.invoke_mock_command("disconnect")
    await command
    assert command.status.is_done
    if command.status.did_succeed:
        assert command.status.did_succeed
    elif command.status.did_fail:
        assert command.status.did_fail
