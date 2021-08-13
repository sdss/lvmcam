import asyncio
import click
from clu import AMQPActor, command_parser
from araviscam import BlackflyCam as blc
import os


async def singleFrame(config, verbose, name, exptime):
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config, verbose=verbose)
    cam = await cs.add_camera(name=name, uid="1")
    exp = await cam.expose(exptime, "LAB TEST")
    await cs.remove_camera(name=name, uid="1")
    filename = f'{name}_{exp.filename}'
    await exp.write(filename=filename)
    return filename


@command_parser.command()
@click.option('--config', type=str, default="./etc/cameras.yaml")
@click.option('--verbose', type=bool, default=True)
@click.argument('name', type=str)
@click.option('--exptime', type=float, default=0.5)
async def main(command, config, verbose, name, exptime):
    filename = await singleFrame(
        config=config,
        verbose=verbose,
        name=name,
        exptime=exptime
    )
    actorPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(actorPath, filename)
    print(filePath)
    command.write('i', text=f"Created {filePath}")
    command.finish()


# class camActor(AMQPActor):
#     def __init__(self):
#         super().__init__(name=(input("actor name(cam): ") or "cam"),
#                          user=(input("username(guest): ") or "guest"),
#                          password=(input("password(guest): ") or "guest"),
#                          host=(input("host(localhost): ") or 'localhost'),
#                          port=(input("port(5672): ") or "5672"),
#                          version='0.1.0')

class camActor(AMQPActor):
    def __init__(self):
        super().__init__(name="cam",
                         user="guest",
                         password="guest",
                         host='localhost',
                         port="5672",
                         version='0.1.0')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


async def runActor():
    CamActor = await camActor().start()
    print(f"{bcolors.OKCYAN}{bcolors.BOLD}Start{bcolors.ENDC}")
    await CamActor.run_forever()


if __name__ == "__main__":
    try:
        asyncio.run(runActor())
    except KeyboardInterrupt:
        print(f"\n{bcolors.OKCYAN}{bcolors.BOLD}Stop{bcolors.ENDC}")
