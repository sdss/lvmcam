#!/bin/bash

# Set umask to 0002 (files are created with rw-rw-r-- permissions)
umask 0002

# Update astropy-iers-data every time the container starts.
cd lvmcam && uv pip install -U astropy-iers-data

# Run the command provided by the user.
exec "$@"
