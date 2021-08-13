import asyncio

async def hello():
    print("Hello")

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


asyncio.run(main())