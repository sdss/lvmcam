FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

## Get some karma ##
LABEL org.opencontainers.image.authors="Florian Briegel, briegel@mpia.de"

# Connect repo to package
LABEL org.opencontainers.image.source="https://github.com/sdss/lvmcam"

WORKDIR /opt

COPY . lvmcam

# Ignore warnings about installing as packages with pip as root.
ENV PIP_ROOT_USER_ACTION=ignore

# uv environment variables
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="$PATH:/opt/lvmcam/.venv/bin"

# Install dependencies to build aravis
RUN apt update -y
RUN apt install -y pkg-config libgirepository1.0-dev \
                   libcairo2-dev gobject-introspection python3-gi \
                   gir1.2-aravis-0.8 aravis-tools aravis-tools-cli \
                   git

# Install lvmcam and dependencies
RUN cd lvmcam && uv sync --frozen --no-cache

COPY ./docker-entrypoint.sh /
RUN ["chmod", "+x", "/docker-entrypoint.sh"]

RUN echo "umask 0002" >> /etc/bash.bashrc

# Run the actor.
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["sh", "-c", "lvmcam $LVMCAM_CONFIG_FILE start --debug"]
