FROM python:3.2-bookworm

## Get some karma ##
LABEL org.opencontainers.image.authors="Florian Briegel, briegel@mpia.de"

# Connect repo to package
LABEL org.opencontainers.image.source="https://github.com/sdss/lvmcam"

WORKDIR /opt

COPY . lvmcam

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="$PATH:/opt/lvmcam/.venv/bin"


RUN apt update -y
RUN apt install -y pkg-config libgirepository1.0-dev \
                   libcairo2-dev gobject-introspection python3-gi \
                   gir1.2-aravis-0.8 aravis-tools aravis-tools-cli \
                   git

RUN pip3 install -U pip setuptools wheel

RUN cd lvmcam && pip3 install .

RUN cd lvmcam && uv sync --frozen --no-cache

# Set umask so that new files inherit the parent folder permissions.
RUN echo "umask 0022" >> /etc/bash.bashrc

CMD ["sh", "-c", "lvmcam $LVMCAM_CONFIG_FILE start --debug"]
