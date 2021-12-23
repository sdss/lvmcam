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

# Docker (Alpha version)

## Build (skymakercam) & Run

```
$ podman build -t sdss/lvmcam ./container --format docker
```

```
$ podman run -d --network=host --name=lvm.cam.sci.agw localhost/sdss/lvmcam
```

```
$ podman run -it --network=host --name=lvm.cam.sci.agw localhost/sdss/lvmcam start --debug
```

```
$ podman run -it --network=host --name=lvm.cam.sci.agw -v /home/user/lvmcam/python/lvmcam:/root/lvmcam/python/lvmcam:rw localhost/sdss/lvmcam start --debug
```

## Pull (skymakercam) & Run

```
$ podman pull ghcr.io/sdss/lvmcam
```

```
$ podman run -d --network=host --name=lvm.cam.sci.agw ghcr.io/sdss/lvmcam
```

```
$ podman run -it --network=host --name=lvm.cam.sci.agw ghcr.io/sdss/lvmcam start --debug
```

```
$ podman run -it --network=host --name=lvm.cam.sci.agw -v /home/user/lvmcam/python/lvmcam:/root/lvmcam/python/lvmcam:rw ghcr.io/sdss/lvmcam start --debug
```

## Delete

```
$ podman kill lvm.cam.sci.agw
$ podman rm lvm.cam.sci.agw
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