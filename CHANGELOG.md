# Changelog

## 1.1.2 - August 10, 2025

### ✨ Improved

- Bump `sdss-basecam` to 0.8.2.


## 1.1.1 - April 1, 2025

### 🔧 Fixed

- Fix a regression in setting the correct umask for new images.


## 1.1.0 - March 18, 2025

### 🔥 Breaking changes

- Require Python 3.10+.

### ✨ Improved

- Update `astropy-iers-data` when the Docker container starts.

### 🔧 Fixed

- Avoid errors while saving images if the IERS tables are not up to date.
- Pin `pygobject==3.50.0` as 3.52 requires `girepository-2.0` which is not provided by Debian Bookworm.


## 1.0.0 - February 27, 2025

### 🔥 Breaking changes

- Removed `araviscam` dependency and move the camera code to `lvmcam`.

### 🔧 Fixed

- Add camera module to documentation and fix actor commands.


## 0.5.0 - January 24, 2025

### 🔧 Fixed

- Use umask 0022 in the container image.

### ⚙️ Engineering

- Use `uv` for dependency management and update the workflows.


## 0.4.14 - September 7, 2024

### 🔧 Fixed

- Fix `additionalProperties: true` not having effect.


## 0.4.13 - July 23, 2024

### ✨ Improved

- [#66](https://github.com/sdss/lvmcam/pull/66) Ensure group write permissions for new files in Docker container.

### 🔧 Fixed

- Fix comment for keyword `REFFILE` being too long when the keyword is populated by `lvmguider`.

### ⚙️ Engineering

- Format and lint using `ruff`.


## 0.4.12 - February 7, 2024

### ✨ Improved

- Added `ISFSWEEP` header keywords to `PROC` extension.


## 0.4.11 - February 4, 2024

### ✨ Improved

- Added `RA`, `DEC`, and `FWHM` header keywords to `PROC` extension.


## 0.4.10 - February 4, 2024

### ✨ Improved

- Add PWI axis keywords.


## 0.4.9 - January 16, 2024

### ✨ Improved

- Support Python 3.12.
- Bump `sdss-basecam` to 0.8.0.

### ⚙️ Engineering

- Update workflow version.


## 0.4.8 - November 5, 2023

### ✨ Improved

- Added `AIRMASS` header keyword.


## 0.4.7 - September 14, 2023

### 🔧 Fixed

- Prevent `PROC` extension header `WCSMODE` default value `none` from being changed to `None`.


## 0.4.6 - September 12, 2023

### ✨ Improved

- Added stub of `PROC` extension to make data model more consistent.


## 0.4.5 - September 10, 2023

### ✨ Improved

- Bumped `araviscam` to 0.2.4.


## 0.4.4 - September 6, 2023

### ✨ Improved

- Bumped `araviscam` to 0.2.3 with a potential fix for the cameras getting into read-only mode.
- Use `umask 0002` in Docker image.


## 0.4.3 - August 31, 2023

### ✨ Improved

- Updated `sdss-araviscam` to 0.2.2.


## 0.4.2 - August 20, 2023

### ✨ Improved

- Added local mean sidereal time header keyword ``LMST``. Note that the value is computed without updated ``IERS-B`` tables so it may be slightly off.
- Reduce the polling of the MoCon.

### ⚙️ Engineering

- Do not add ``skymakercam`` to docker image.


## 0.4.1 - August 13, 2023

### ✨ Improved

- Upgraded `araviscam` to 0.2.1 with workarounds for exposures with empty buffers.


## 0.4.0 - August 11, 2023

### 🔥 Breaking changes

- This version drops support for `skymakercam`. Use the `0.3.x` tags if necessary.

### ✨ Improved

- [#56](https://github.com/sdss/lvmscp/pull/56) Serious rewrite of the codebase with relatively limited changes in behaviour. A lot of code that overrode the default behaviour in `basecam` has been removed.
- Added a custom `reconnect` command that will reconnect both cameras even if they were not present when the actor started.


## 0.3.5 - July 9, 2023

### ✨ Improved

- Use `basecam 0.7.2` with `CLU 2.1.0`. Adds the `get-command-model` command.
- Build docker image using `python:3.9-bookworm` base image. This installs a more recent version of the Aravis libraries and seems to solve several camera communication issues.
- Fixed East cameras flips.


## 0.3.1 - March 10, 2023

### 🏷️ Changed

- Change image destination to `/data/agcam/<SJD>/<CAMERA>_<SEQ_NO>.fits`.


## 0.3.0 - March 10, 2023

### ✨ Improved

- Move [lvmtel](http://github.com/sdss/lvmtel) to its own repo.
- Linting and some code cleaning.
- Update Dockerfile to deploy at LCO.


## 0.2.4 - January 24, 2022

### ✨ Improved

- Add [cluplus](https://github.com/sdss/cluplus)



## 0.2.3 - December 23, 2021

### ✨ Improved

- Add Docker


## 0.2.2 - December 13, 2021

### ✨ Improved

- Issue #49 (Add support for virtual cameras)
  - Delete `-t`, `-i` option in `connect` command.
  - Add `camtype.yaml` in `python/lvmcam/etc` for selecting between real(araviscam) and virtual(skymakercam) camera.
  - Put `type` property in `cameras.yaml`


## 0.2.1 - December 12, 2021

### ✨ Improved

- Issue #44 (Add actor command for extra fits header parameters)
  - Add `-h` or `--header` option similar to [archon](https://github.com/sdss/archon/blob/c28080d145072dc80dedff111d6d589a7fd195ff/archon/actor/commands/expose.py#L145)


## 0.2.0 - December 3, 2021

### 🚀 New & ✨ Improved

- Issue #41 (Use the basecam.Actor)
  - `LvmcamBaseActor(BaseActor)` -> `LvmcamBaseActor(BaseCameraActor)`
- Issue #42 (Use basecam.Imagenamer)
  - Remove `--filepath` or `-p` option in `expose` command.
  - Put `path` property in `cameras.yaml`.
  - Change how to make image name.
- Issue #43 (Use basecam fits compression through model)
  - Remove fpack in source code.
  - Change lists of `-c` option to same lists in astropy’s [CompImageHDU](https://docs.astropy.org/en/latest/io/fits/api/images.html#astropy.io.fits.CompImageHDU).
- Issue #44 (Add actor command for extra fits header parameters)
  - Add `-eh` or `--extraheader` option for making extra fits header.
  - Put `extrahdr` property in `cameras.yaml`
- Issue #45 (Return of expose)
  - Put `PATH=path_dict` in `command.finish()` instead of `command.info()`
- Issue #46 (Indexing for expose testshot mode)
  - Fix it by using basecam.Imagenamer(#42)
- Issue #47 (File saving of multiple images)
  - Remove `make_file` function and Write images to disk immediately.


## 0.1.4 - November 15, 2021

### ✨ Improved

- Add `-c` option in expose command to compress fits file. For more detail, visit [fpack & funpack](https://heasarc.gsfc.nasa.gov/fitsio/fpack/).


## 0.1.3 - November 2, 2021

### ✨ Improved

- Change log when `-v` option is provided.


## 0.1.2 - November 1, 2021

### ✨ Improved

- Reflect update of [sdss/araviscam](https://github.com/sdss/araviscam) version 0.0.301.


## 0.1.1 - October 25, 2021

### 🚀 New

- Restore returned values of actor commands similar to before 0.1.0 version.
  - Add JSON schema

### ✨ Improved

- Change unit testing code so that JSONActor is not used.


## 0.1.0 - October 11, 2021

### 🚀 New

- Change returned values of actor commands because of update of [sdss-clu 1.3.0](https://clu.readthedocs.io/en/latest/changelog.html#september-17-2021)

### ✨ Improved

- Code Refactoring


## 0.0.5 - October 5, 2021

### ✨ Improved

- First unit testing
- Delete unnecessary directories and files(filr/\*, comutest/) in python/lvmcam/


## 0.0.4 - September 29, 2021

### 🚀 New

- Reflect update of sdss/araviscam on Sep 28, 2021.
  - Add properties such as pixsize and pixcal in cameras.yaml
  - Add headers such as CRPIX1, CRPIX2, CUNIT1, CUNIT2, CTYPE1, CTYPE2, CRVAL1, CRVAL2, CD1_1, CD2_2, CD1_2, and CD2_1.
  - Add options in `lvmcam expose` such as `-r`, `-d`, `-K`. This options are respectively RA J2000 (deg), Dec J2000 (deg), and K-mirror angle (deg).
- Rename versions.


## 0.0.3 - September 24, 2021

### 🔧 Fixed

- Fix errors that occurs when `lvmcam start` runs without `--debug` option.


## 0.0.2 - September 13, 2021

### 🚀 New

- Add options for test.
  - `lvmcam connect --test`: add virtual camera
  - `expose --testshot EXPTIME NUM CAMNAME`: Test shot


## 0.0.1 - September 6, 2021

### 🚀 New

- Initial version of lvmcam.
- Basic features.
  - Show status of cameras.
  - Connect/Disconnect cameras.
  - Take exposure pictures by using custom parameters.
  - Save fits files and return absolute file paths in list type.
