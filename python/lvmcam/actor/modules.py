import datetime
import os

import asyncio
import time

import astropy

from sdsstools import get_logger
from sdsstools.logger import SDSSLogger
from typing import cast
import logging

logger_name = __name__.upper()
log_header = f"[{logger_name.upper()}]: "
logger = cast(SDSSLogger, get_logger(logger_name))

log_header = ""
logger: SDSSLogger


def log(message, level=logging.DEBUG, use_header=True):
    """Logs a message with a header."""
    global log_header
    global logger
    header = (log_header or "") if use_header else ""
    logger.log(level, header + message)


# def timeit(func):
#     async def process(func, *args, **params):
#         if asyncio.iscoroutinefunction(func):
#             # print("this function is a coroutine: {}".format(func.__name__))
#             return await func(*args, **params)
#         else:
#             # print("this is not a coroutine")
#             return func(*args, **params)

#     async def helper(*args, **params):
#         # print("{}.time".format(func.__name__))
#         start = time.time()
#         result = await process(func, *args, **params)

#         # Test normal function route...
#         # result = await process(lambda *a, **p: print(*a, **p), *args, **params)

#         log(f"[{func.__name__}]: {(time.time() - start):.3f} s")
#         return result

#     return helper


def atimeit(func):
    # async def process(func, *args, **params):
    #     if asyncio.iscoroutinefunction(func):
    #         # print("this function is a coroutine: {}".format(func.__name__))
    #         return await func(*args, **params)
    #     else:
    #         # print("this is not a coroutine")
    #         return func(*args, **params)

    async def timed(*args, **params):
        start = time.time()
        result = await func(*args, **params)
        dt = time.time() - start
        a = "async"
        log(
            f"[{bcolors.OKCYAN}{bcolors.BOLD}{dt:.3f}{bcolors.ENDC} s]: {bcolors.OKGREEN}{bcolors.BOLD}{a}{bcolors.ENDC} {func.__name__}"
        )
        return result

    return timed


def timeit(func):
    def timed(*args, **params):
        start = time.time()
        result = func(*args, **params)
        dt = time.time() - start
        log(
            f"[{bcolors.OKCYAN}{bcolors.BOLD}{dt:.3f}{bcolors.ENDC} s]: {func.__name__}"
        )
        return result

    return timed


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# def pretty(time):
#     return f"{bcolors.OKCYAN}{bcolors.BOLD}{time}{bcolors.ENDC}"


# def pretty2(time):
#     return f"{bcolors.OKGREEN}{bcolors.BOLD}{time}{bcolors.ENDC}"


# def current_progress(file, string_to_show):
#     current_time = pretty(datetime.datetime.now())
#     current_filename = os.path.basename(file)
#     return f"{current_time} |{current_filename}| {string_to_show}"


def change_dir_for_normal_actor_start(file):
    os.chdir(os.path.dirname(file))
    os.chdir("../")
    os.chdir("../")
    os.chdir("../")
    os.chdir("../")


# def trace(func):
#     def wrapper():
#         print(func.__name__, "start")
#         func()
#         print(func.__name__, "done")

#     return wrapper

class variables():
    targ = None
    cs = None
    cs_list = []
    cam_list = []
    # dev_list = {}
    camdict = {}
    camname = None
    kmirr = None
    flen = None
    config = None
    Aravis_available_camera = {}
    # camtypename = None


# @modules.timeit
def make_targ_from_ra_dec(ra, dec):
    if ra is not None and dec is not None:
        if ra.find("h") < 0:
            # apparently simple floating point representation
            targ = astropy.coordinates.SkyCoord(
                ra=float(ra), dec=float(dec), unit="deg"
            )
        else:
            targ = astropy.coordinates.SkyCoord(ra + " " + dec)
    else:
        targ = None
    return targ
