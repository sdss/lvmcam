# lvmcam

![Versions](https://img.shields.io/badge/python->3.8-blue)
[![Test](https://github.com/sdss/lvmcam/actions/workflows/test.yml/badge.svg)](https://github.com/sdss/lvmcam/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/sdss-lvmcam/badge/?version=latest)](https://sdss-lvmcam.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/sdss/lvmcam/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/lvmcam)

The package for [lvmagp](https://github.com/sdss/lvmagp).

# See also
- [clu](https://github.com/sdss/clu)
- [archon](https://github.com/sdss/archon)
- [basecam](https://github.com/sdss/basecam)
- [araviscam](https://github.com/sdss/araviscam)
- [skymakercam](https://github.com/sdss/skymakercam)
- [LVM_FLIR_Software](https://github.com/sdss/LVM_FLIR_Software)

# Docker (Beta version)

## Download
```
$ git clone https://github.com/sdss/lvmcam
$ cd lvmcam
$ poetry install
```

## Run
```
$ poetry run container_start
```

Run container with killing current instance
```
$ poetry run container_start --kill
```

Run container with custom name (default name = lvm.cam)
```
$ poetry run container_start --name=lvm.cam.sci.agw
```

Run container with lvmcam debug mode
```
$ poetry run container_start --debug
```

Run container with virtual camera (skymakercam) mode
```
$ poetry run container_start --virtual
```

Run multiple containers
```
$ poetry run container_start --name=lvm.cam.sci.agw
$ poetry run container_start --name=lvm.cam.sci.age
$ poetry run container_start --name=lvm.cam.sci.agc
```

## Build
```
$ poetry run container_build
```

Build from scratch
```
$ poetry run container_build --no-cache
```