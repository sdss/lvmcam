# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: __main__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import time
import random
import string
import uuid
import argparse

import asyncio
from datetime import datetime as dt
import aio_pika as apika

from clu.client import AMQPClient, AMQPReply

from astropy.io import fits

# hard exit
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from simple_plotit import PlotIt

class AMQPClientUI(AMQPClient):
    
    def __init__(
        self,
        argv,
        ploit,
        *args,
        **kwargs
    ):
       self.camactor = argv.camera_actor
       self.camnames = {argv.west: 0, argv.east: 1}

       self.kmactor = argv.km_actor

       self.plotit = ploit

       super().__init__(f"{self.camactor}_ui-{uuid.uuid4().hex[:8]}", *args, **kwargs)

    async def handle_reply(self, message: apika.IncomingMessage) -> AMQPReply:
        """Handles a reply received from the exchange.
        """
        reply = AMQPReply(message, log=self.log)
        if self.camactor == reply.sender:
            for camreply in reply.body:
                if reply.body[camreply].get("state", None) == "written":
                    filename = reply.body[camreply].get("filename", None)
                    data = fits.open(filename)[0].data
                    self.plotit.update(self.camnames[camreply], data)
        elif self.kmactor == reply.sender:
            print(reply.body)

async def main(loop, args):
   plotit = PlotIt(title=[f"{args.camera_actor} {args.west}", f"{args.camera_actor} {args.east}"])
   client = await AMQPClientUI(args, plotit, host='localhost').start()
   
   while(True):
        await asyncio.sleep(0.001)
        plotit.start_event_loop(0.001)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", '--camera_actor', type=str, default="lvm.sci.agcam", help="Choose your camera")
    args = parser.parse_args()
    parser.add_argument("-k", '--km_actor', type=str, default="lvm.sci.km", help="Choose your kmirror")
    args = parser.parse_args()
    parser.add_argument("-w", '--west', type=str, default="west", help="Choose your west camera name")
    args = parser.parse_args()
    parser.add_argument("-e", '--east', type=str, default="east", help="Choose your east camera name")
    args = parser.parse_args()

    # Start the server
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop, args))
    print("waiting ...")
    loop.run_forever()
    print("exit ...")


