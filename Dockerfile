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
RUN apt install -y build-essential pkg-config gir1.2-girepository-2.0 \
                   libcairo2-dev gobject-introspection python3-gi git \
                   meson zlib1g libxml2 libxml2-dev

# Build and install aravis 0.8.34
RUN git clone https://github.com/AravisProject/aravis.git
RUN cd aravis && git checkout 0.8.34
RUN cd aravis && meson setup build && cd build && ninja && ninja install

# Install lvmcam and dependencies
RUN cd lvmcam && uv sync --frozen --no-cache

# Set environment variables for GI to find the aravis library
ENV GI_TYPELIB_PATH="/usr/local/lib/x86_64-linux-gnu/girepository-1.0"
ENV LD_LIBRARY_PATH="/usr/local/lib/x86_64-linux-gnu"

COPY ./docker-entrypoint.sh /
RUN ["chmod", "+x", "/docker-entrypoint.sh"]

# Run the actor.
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["sh", "-c", "lvmcam $LVMCAM_CONFIG_FILE start --debug"]
