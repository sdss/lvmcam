from araviscam import BlackflyCam as blc

async def singleFrame(config, verbose, name, uid, exptime):
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config, verbose=verbose)
    cam = await cs.add_camera(name=name, uid=uid)
    exp = await cam.expose(exptime=exptime)
    filename = f'{name}_{exp.filename}'
    await exp.write(filename=filename)
    return filename