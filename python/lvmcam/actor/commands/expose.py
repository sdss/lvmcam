# @Author: Mingyu Jeon (mgjeon@khu.ac.kr)
# @Date: 2021-08-23
# @Filename: expose.py

from __future__ import absolute_import, annotations, division, print_function
import click
from click.decorators import command
from clu.command import Command
from . import parser

# exposure function
import asyncio
import os
from araviscam.araviscam import BlackflyCam as blc
async def exposure(exptime, name, num, filepath, config, overwrite):
    cs = blc.BlackflyCameraSystem(blc.BlackflyCamera, camera_config=config)
    cam = await cs.add_camera(name=name, uid=cs._config['sci.agw']['uid'])
    paths = []
    for i in range(num):
        exp = await cam.expose(exptime=exptime)
        filepath = os.path.abspath(filepath)
        exp.filename = f'{name}_{exp.filename}'
        paths.append(os.path.join(filepath, exp.filename))
        try:
            await exp.write(filename=paths[i], overwrite=overwrite)
        except OSError:
            await cs.remove_camera(name=name, uid=cs._config['sci.agw']['uid'])
            return "Error"
    await cs.remove_camera(name=name, uid=cs._config['sci.agw']['uid'])
    return paths

# plot fits file funciton
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
plt.style.use(astropy_mpl_style)
def plot_fits(file):
    data, header = fits.getdata(file, header=True)
    fits_inf = fits.open(file)
    print(fits_inf.info())
    image_data = fits_inf[0].data[0]
    plt.figure()
    plt.imshow(image_data, cmap='gray')
    # plt.axis('off')
    # plt.grid(b=None)
    plt.colorbar()
    plt.show()
    plt.close()

# actor
__all__ = ["expose"]

@parser.group()
def expose(*args):
    """[TEST] expose function of araviscam module."""
    pass

@expose.command()
@click.argument("EXPTIME", type=float)
@click.argument('NAME', type=str)
@click.argument('NUM', type=int)
@click.argument("FILEPATH", type=str, default="python/lvmcam/assets")
@click.argument('CONFIG', type=str, default="python/lvmcam/etc/cameras.yaml")
@click.option('--overwrite', type=bool, default=False)
@click.option('--plot', type=bool, default=False)
async def start(
    command: Command,
    exptime: float,
    name: str,
    num: int,
    filepath: str,
    config: str,
    overwrite: bool,
    plot: bool,
):
    paths = []

    try:
        paths = await exposure(
            exptime=exptime,
            name=name,
            num=num,
            filepath=filepath,
            config=config,
            overwrite=overwrite
        )
    except OSError:
        command.info("File alreday exists. See traceback in the log for more information.")
        command.info("If you want to overwrite the file, set --overwrite True.")
        command.finish(path="OSError", info="File alreday exists. See traceback in the log for more information.")
        return

    if (paths != "Error"):
        # command.info(f"Created {paths}")
        command.finish(path=paths)
        if plot:
            plot_fits(paths[-1])
        return
    else:
        command.finish(path="File already exists")
        return
