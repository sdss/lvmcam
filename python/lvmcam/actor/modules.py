import datetime
import os


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


def pretty(time):
    return f"{bcolors.OKCYAN}{bcolors.BOLD}{time}{bcolors.ENDC}"


def current_progress(file, string_to_show):
    current_time = pretty(datetime.datetime.now())
    current_filename = os.path.basename(file)
    return f"{current_time} |{current_filename}| {string_to_show}"


def change_dir_for_normal_actor_start(file):
    os.chdir(os.path.dirname(file))
    os.chdir("../")
    os.chdir("../")
    os.chdir("../")
    os.chdir("../")


def trace(func):
    def wrapper():
        print(func.__name__, "start")
        func()
        print(func.__name__, "done")

    return wrapper
