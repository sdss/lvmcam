#!/usr/bin/env python3.9

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

import yaml

from typing import Dict

from datetime import datetime as dt
import aio_pika as apika


# hard exit
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from astropy.coordinates import SkyCoord
import astropy.units as u

from clu.client import AMQPClient, AMQPReply

from cluplus.proxy import flatten

default = """
scraper:
    lvm.sci.pwi:
        ra_j2000_hours: raj2000__h
        dec_j2000_degs: decj2000__d
        altitude_degs: altitude_d
        azimuth_degs: azimuth_d

    lvm.sci.foc:
        Position: foc_dt

    lvm.sci.km:
        Position: km_d

    lvm.sci.tel:
        temperature: bentemp
        humidity: benhum
        pressure: benpress

    lvm.sci.agcam:
        east.temperature: east.temp
        east.filename: east.file
        west.temperature: west.temp
        west.filename: west.file
        
    lvm.spec.agcam:
        center.temperature: center.temp
        center.filename: center.file

"""

class ScraperDataStore(object):
    def __init__(self, config={}):
        self.actor_key_maps = config
        self.data = {}

    def copy(self):
        o = type(self).__new__(self.__class__)
        o.actor_key_maps = self.actor_key_maps.copy()
        o.data = self.data.copy()
        return o

    def __repr__(self):
        return self.data.__repr__()

    def keys(self):
         return self.data.keys()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def actors(self):
        return list(self.actor_key_maps.keys()) if self.actor_key_maps else []

    def set(self, key, val, timestamp=dt.utcnow()):
        self.data[key] = (val, timestamp)
        
    def get(self, key, default=None):
        return self.data.get(key, (default, None))[0]
        
    def update(self, data:dict, timestamp=dt.utcnow()):
        self.data.update({k:(v, timestamp) for k, v in data.items()})

    def update_with_actor_key_maps(self, actor, data:dict, timestamp=dt.utcnow()):
        akm = self.actor_key_maps.get(actor, None)
        self.data.update({akm[k]:(v, timestamp) for k, v in data.items() if k in akm.keys()})

    def items(self):
        return self.data.items()
   

class AMQPMonitor(AMQPClient):
    
    def __init__(
        self,
        argv,
        *args,
        **kwargs
    ):

        super().__init__(f"monitor-{uuid.uuid4().hex[:8]}", *args, config=yaml.safe_load(default), **kwargs)

        self.scraper_store = ScraperDataStore(self.config.get("scraper", {}))


    async def handle_reply(self, message: apika.IncomingMessage) -> AMQPReply:
        """Handles a reply received from the exchange.
        """
        reply = AMQPReply(message, log=self.log)
        if reply.sender in self.scraper_store.actors() and reply.headers.get("message_code", None) in ":i":
            timestamp = apika.message.decode_timestamp(message.timestamp) if message.timestamp else datetime.utcnow()
            self.scraper_store.update_with_actor_key_maps(reply.sender, flatten(reply.body), timestamp)

        return reply

async def main(loop, args):
   client = await AMQPMonitor(args, host=args.rmq_host).start()
   log = client.log

   log.debug("waiting ...")
   while(True):
        await asyncio.sleep(0.5)
        print('\033[2J')
        for k, v in client.scraper_store.items():
            if isinstance(v[0], (int, float)):
#                print(f"\033[1m{k:14}: {v[0]:10.2f}\033[21m ({v[1]})")
                print(f"\033[34m{k:14}\033[0m: \033[32m{v[0]:10.2f}\033[0m ({v[1]})")
            else:
#                print(f"\033[1m{k:14}: {v[0]}\033[21m ({v[1]})")
                print(f"\033[34m{k:14}\033[0m: \033[32m{v[0]}\033[0m ({v[1]})")
            
        print()

#\033[34m [34mBlue[0m
#\033[32m [32mGreen[0m
                        
                        
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", '--rmq_host', type=str, default="localhost", help="Choose your rabbitmq host")
    args = parser.parse_args()

    # Start the server
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop, args))
    loop.run_forever()


