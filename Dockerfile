FROM python:3.9-bullseye

## Get some karma ##
MAINTAINER Florian Briegel, briegel@mpia.de

# Connect repo to package
LABEL org.opencontainers.image.source https://github.com/sdss/lvmcam

WORKDIR /root

COPY . lvmcam

RUN apt update -y
RUN apt install -y pkg-config libgirepository1.0-dev \
                   libcairo2-dev gobject-introspection python3-gi \
                   gir1.2-aravis-0.8 aravis-tools aravis-tools-cli \
                   git

RUN pip3 install -U pip setuptools wheel

RUN cd lvmcam && pip3 install .

# This is temporary, but the tagged/PyPI versions that lvmcam installs are
# quite out of date and won't work. We use the main branch.

RUN git clone https://github.com/sdss/araviscam
RUN git clone https://github.com/sdss/skymakercam

RUN cd araviscam && pip3 install .
RUN cd skymakercam && pip3 install .

COPY ./run-actor.sh .

# Need to remove the cloned repos because run-actor imports lvmcam to
# get its path and if the directory is there it will import it locally
# instead of using the site-packages one.

RUN rm -Rf lvmcam araviscam skymakercam

CMD ["/root/run-actor.sh"]
