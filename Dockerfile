FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

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
RUN apt install -y build-essential pkg-config libgirepository1.0-dev \
                   libcairo2-dev gobject-introspection python3-gi git \
                   meson zlib1g libxml2 glib2.0

# Build aravis
RUN git clone https://github.com/AravisProject/aravis.git
RUN cd aravis && meson setup build && meson install build

RUN cd lvmcam && uv sync --frozen --no-cache

# Set umask so that new files inherit the parent folder permissions.
RUN echo "umask 0022" >> /etc/bash.bashrc

CMD ["sh", "-c", "lvmcam $LVMCAM_CONFIG_FILE start --debug"]
