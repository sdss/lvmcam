# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: __main__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import argparse
import asyncio
import random

# hard exit
import signal
import string
import time
import uuid
from datetime import datetime as dt

import aio_pika as apika
from astropy.io import fits
from clu.client import AMQPClient, AMQPReply


# from astropy.utils import iers
# iers.conf.auto_download = False


signal.signal(signal.SIGINT, signal.SIG_DFL)

import astropy.units as u
from astropy.coordinates import SkyCoord
from simple_plotit import PlotIt


class AMQPClientUI(AMQPClient):
    def __init__(self, argv, ploit, *args, **kwargs):
        self.cam_actor = argv.camera_actor
        self.cam_names = {argv.west: 0, argv.east: 1}

        self.km_actor = argv.km_actor
        self.tel_actor = argv.tel_actor

        self.plotit = ploit
        self.radec = None
        self.kmangle = None

        super().__init__(f"{self.cam_actor}_ui-{uuid.uuid4().hex[:8]}", *args, **kwargs)

    async def handle_reply(self, message: apika.IncomingMessage) -> AMQPReply:
        """Handles a reply received from the exchange."""
        reply = AMQPReply(message, log=self.log)
        self.log.debug(f"{reply.sender} {reply.body}")
        if self.cam_actor == reply.sender:
            for cam_reply in reply.body:
                if cam_reply not in self.cam_names:
                    continue
                if reply.body[cam_reply].get("state", None) == "written":
                    filename = reply.body[cam_reply].get("filename", None)
                    data = fits.open(filename)[0].data.byteswap().newbyteorder()
                    if len(data.shape) == 3:
                        data = data[0]
                    self.plotit.update(
                        self.cam_names[cam_reply], data, self.radec, self.kmangle
                    )

        elif self.km_actor == reply.sender:
            if "Position" in reply.body:
                self.kmangle = reply.body["Position"]
                self.log.debug(f'{reply.body["Position"]}')

        elif self.tel_actor == reply.sender:
            if "ra_j2000_hours" in reply.body:
                self.radec = SkyCoord(
                    ra=reply.body["ra_j2000_hours"] * u.hour,
                    dec=reply.body["dec_j2000_degs"] * u.deg,
                )
                self.log.debug(f"{self.radec}")

        else:
            return


async def main(loop, args):
    plotit = PlotIt(
        title=[f"{args.camera_actor} {args.west}", f"{args.camera_actor} {args.east}"],
        site=args.site,
    )
    client = await AMQPClientUI(args, plotit, host=args.rmq_host).start()
    log = client.log

    log.debug("waiting ...")
    while True:
        await asyncio.sleep(0.01)
        plotit.start_event_loop(0.01)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--camera_actor",
        type=str,
        default="lvm.sci.agcam",
        help="Choose your camera",
    )
    parser.add_argument(
        "-k", "--km_actor", type=str, default="lvm.sci.km", help="Choose your kmirror"
    )
    parser.add_argument(
        "-t",
        "--tel_actor",
        type=str,
        default="lvm.sci.pwi",
        help="Choose your telescope",
    )
    parser.add_argument(
        "-w", "--west", type=str, default="west", help="Choose your west camera name"
    )
    parser.add_argument(
        "-e", "--east", type=str, default="east", help="Choose your east camera name"
    )
    parser.add_argument(
        "-s", "--site", type=str, default="LCO", help="Choose your site"
    )
    parser.add_argument(
        "-H",
        "--rmq_host",
        type=str,
        default="localhost",
        help="Choose your rabbitmq host",
    )
    args = parser.parse_args()

    # Start the server
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop, args))
    loop.run_forever()
