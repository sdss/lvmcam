import subprocess
# import sys
import os
# import time
# import pexpect
import shlex
import click
import socket
from pathlib import PosixPath

container_bin = 'podman'
lvmt_root = os.environ["PWD"]
lvmt_image_source_local = "localhost/sdss"
lvmt_image_source_remote = "ghcr.io/sdss"
lvmt_image_name = 'lvmcam'

default_cam = 'lvm.cam'

# def isRunning(name: str = default_cam):
#     command = subprocess.run(shlex.split(f"{container_bin} container exists {name}"))
#     return not command.returncode # True if running

# def next_free_port( port=5900, max_port=5909 ):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     while port <= max_port:
#         try:
#             sock.bind(('', port))
#             sock.close()
#             return port
#         except OSError:
#             port += 1
#     print('no free ports')
#     return None

@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--use-cache/--no-cache", default=True)
def build(lvmt_root:str, use_cache: bool):
    cam_dockerfile = f"{lvmt_root}/container"
    lvmt_image_fullbuild = "" if use_cache else " --no-cache"
    build = f"{container_bin} build --tag sdss/{lvmt_image_name} {lvmt_image_fullbuild} --rm {cam_dockerfile} --format docker"
    print(build)
    command = subprocess.run(shlex.split(build))


# @click.command()   
# @click.option("--name", "-n", default=default_cam, type=str)
# @click.option("--debug", "-d", default=False, type=bool)
# def autotuner(name: str, debug:bool):
#     run_autotuner = f"-v {lvmt_root}:/root/lvmt:Z -e cam_NAME={name}"
#     run = f"{container_bin} exec -ti {name} /opt/autotuner-1.0.3beta1/run-autotuner_nogl"
#     command = subprocess.run(shlex.split(f"{run}"))

# podman build -t sdss/lvmcam ./container --format docker
# podman kill lvm.cam.sci.agw
# podman run --rm -d --network=host --name=lvm.cam.sci.agw localhost/sdss/lvmcam

@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--name", "-n", default=default_cam, type=str)
@click.option("--virtual/--no-virtual", "-v", default=False)
@click.option("--debug/--no-debug", "-d", default=False)
@click.option("--kill/--no-kill", default=False)
def start(lvmt_root:str, name: str, virtual:bool, debug:bool, kill:bool):
    if not subprocess.run(shlex.split(f"podman image exists {lvmt_image_source_local}/{lvmt_image_name}")).returncode:
       lvmt_image = f"{lvmt_image_source_local}/{lvmt_image_name}"
    else:
       if subprocess.run(shlex.split(f"podman image exists {lvmt_image_source_remote}/{lvmt_image_name}")).returncode:
           subprocess.run(shlex.split(f"podman pull {lvmt_image_source_remote}/{lvmt_image_name}:latest"))
       lvmt_image = f"{lvmt_image_source_remote}/{lvmt_image_name}"
    # vnc_port=None

    if kill:
        subprocess.run(shlex.split(f"podman kill {name}"))
        subprocess.run(shlex.split(f"podman rm {name} -f"))

        
    run_base = f"--rm -td --network=host --name={name} -e HOME_PATH={os.getcwd()}"
    
    run_base += f" -e LVMT_RMQ={socket.gethostname()}"

    # run_base += f" -e LVMT_PATH={os.path.dirname(lvmt_root)}"
    
    # vnc_port = next_free_port()
    # run_base +=  f" -p {vnc_port}:5900 -e cam_GEOM={geom}"
        
    if virtual:
        run_base +=  f" -e CAM_VIRTUAL=true"

    if debug:
        run_base +=  f" -e CAM_DEBUG=true"

    # run_base += " -v /dev:/dev:rslave"
    
    # system_xauthority=PosixPath('~/.Xauthority').expanduser()
    run_cam = f"-v {lvmt_root}/python/lvmcam:/root/lvmcam/python/lvmcam:rw -e CAM_NAME={name}"
    run = f"{container_bin} run {run_base} {run_cam} {lvmt_image}"
    print(run)
    #child = pexpect.spawn(run)
    #child.expect('BSC loaded')
    #assert isRunning(name) == True
    command = subprocess.run(shlex.split(f"{run}"))
    logs = subprocess.run(shlex.split(f"podman logs -f {name}"))
    # if vnc_port and os.environ.get("DISPLAY") and system_xauthority:
    #     vncclient = subprocess.run(shlex.split(f"vncviewer :{vnc_port - 5900}"))
    
    print("done")

@click.command()   
@click.option("--name", "-n", default=default_cam, type=str)
def stop(name: str):
    command = subprocess.run(shlex.split(f"{container_bin} kill {name}"))

