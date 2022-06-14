FROM ubuntu:20.04

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

# podman  build --tag ubuntu_lvmt_cam --rm .

# podman run -ti --rm --name lvmt_cam -v .:/root/lvmt:Z -P localhost/ubuntu_lvmt_cam

RUN apt update -y && \
    apt install -y wget && \
    echo "8\n7\n" | apt install -y software-properties-common && \
    echo "30\n1\n" | apt install -y keyboard-configuration && \
    wget -qO - https://svn.mpia.de/repo/linux/ubuntu/archive.key | apt-key add - && \
    echo "deb https://svn.mpia.de/repo/linux/ubuntu focal main" > /etc/apt/sources.list.d/mpia.list

RUN apt update -y

RUN apt install -y sudo git lsof pkg-config libgirepository1.0-dev libcairo2-dev
RUN apt install -y gir1.2-aravis-0.8 aravis-tools aravis-tools-cli
 
RUN apt install -y python3-pip
RUN pip3 install sdss-clu sdss-basecam sdss-araviscam sdss-skymakercam expandvars


WORKDIR /root

#COPY run-cam.sh /root

CMD ["/root/lvmcam/container/run-cam.sh"]



