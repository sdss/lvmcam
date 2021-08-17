import asyncio
import click
from clu import AMQPActor, command_parser


@command_parser.command()
@click.option('--overwrite', type=bool, default=False)
async def expose(command, overwrite):
    """Exposes the camera."""

    command.info(text='Starting the exposure.')

    lvmcam_cmd = await command.actor.send_command(
        'lvmcam',
        'singleframe',
        'singleexpose',
        f'--overwrite {overwrite}'
    )
    await lvmcam_cmd
    if lvmcam_cmd.status.did_fail:
        return command.fail(error="lvmcam failed to open")

    replies = lvmcam_cmd.replies
    fits_path = replies[-1].body["path"]

    if (fits_path == "OSError"):
        return command.fail(error="File Already Exists")

    command.info(f"File created in {fits_path!r}.")
    return command.finish(text='Exposure done!')


class CameraActor(AMQPActor):
    def __init__(self):
        super().__init__(
            name="testagp",
            user="guest",
            password="guest",
            host="localhost",
            port=5672,
            version="0.1.0"
        )


async def main():
    actor = await CameraActor().start()
    await actor.run_forever()

asyncio.run(main())
