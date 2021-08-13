import asyncio
import click
from clu import AMQPActor, command_parser


@command_parser.command()
@click.argument("name", type=str)
async def agps(command, name):
    command.info(text=f"Hello {name}")
    print(name)
    return command.finish(text="Exposure done!")


class CameraActor(AMQPActor):
    def __init__(self):
        super().__init__(
            name="agp",
            user="guest",
            password="guest",
            host="localhost",
            port=5672,
            version="0.1.0",
        )


async def run_actor():
    actor = await CameraActor().start()
    await actor.run_forever()


asyncio.run(run_actor())