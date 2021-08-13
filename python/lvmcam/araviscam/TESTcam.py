import asyncio
import click
from clu import AMQPActor, command_parser

@command_parser.command()
@click.argument('name', type=str)
async def cams(command, name):
    filename = 'file'+name
    command.write('i', text=f"Created {filename}")
    # await(await command.actor.send_command("agp", "agps", filename))
    await(await command.actor.send_command("cam", "main", filename))
    command.finish()

class camActor(AMQPActor):
        def __init__(self):
            super().__init__(
                name="cam2",
                user="guest",
                password="guest",
                host="localhost",
                port=5672,
                version="0.1.0",
            )

async def run_actor():
    actor = await camActor().start()
    await actor.run_forever()

asyncio.run(run_actor())