import asyncio
import click
from clu import AMQPActor, command_parser
from araviscam import BlackflyCam as blc
import os

async def singleFrame(config, verbose, name, uid, exptime):
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config, verbose=verbose)
    cam = await cs.add_camera(name=name, uid=uid)
    exp = await cam.expose(exptime=exptime)
    filename = f'{name}_{exp.filename}'
    await exp.write(filename=filename)


async def main():
    task = []

    task.append(singleFrame(
            config="./etc/cameras.yaml",
            verbose=True,
            name="lab",
            uid="19283193",
            exptime=0.1
        ))

    task.append(singleFrame(
            config="./etc/cameras.yaml",
            verbose=True,
            name="lab",
            uid="19283193",
            exptime=0.1
        ))
    tasks = asyncio.create_task(task)
    tasks.cancle()
    await asyncio.gather(*task)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
