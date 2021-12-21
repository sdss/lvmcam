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

# Docker (for Ping-pong Test)

## Build & Run
```
$ git clone https://github.com/sdss/lvmcam
$ cd lvmcam
$ podman build -t sdss/lvmcam ./container --format docker
$ podman run -d --network=host --name=lvm.cam.sci.agw localhost/sdss/lvmcam
```

## Start & Stop

```
$ podman start lvm.cam.sci.agw
$ podman stop lvm.cam.sci.agw
```

## Status

```
$ podman ps (-a)
```

## Delete Container

```
$ podman kill lvm.cam.sci.agw
$ podman rm lvm.cam.sci.agw
```