# Changelog

## 0.3.0 - March 10, 2023

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
