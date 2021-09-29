# Changelog

## 0.0.4 - September 29, 2021

### 🚀 New
* Reflected update of sdss/aravisca on Sep 28, 2021.
    * Added properties such as pixsize and pixcal in cameras.yaml
    * Added headers such as CRPIX1, CRPIX2, CUNIT1, CUNIT2, CTYPE1, CTYPE2, CRVAL1, CRVAL2, CD1_1, CD2_2, CD1_2, and CD2_1.
    * Added options in `lvmcam expose` such as `-r`, `-d`, `-K`. This options are respectively RA J2000 (deg), Dec J2000 (deg), and K-mirror angle (deg).
* Rename versions.

## 0.0.3 - September 24, 2021

### 🔧 Fixed

* Fixed errors that occurs when `lvmcam start` runs without `--debug` option.


## 0.0.2 - September 13, 2021

### 🚀 New

* Added options for test.
    * `lvmcam connect --test`: add virtual camera
    * `expose --testshot EXPTIME NUM CAMNAME`: Test shot

## 0.0.1 - September 6, 2021

### 🚀 New

* Initial version of lvmcam.
* Basic features.
    * Show status of cameras.
    * Connect/Disconnect cameras.
    * Take exposure pictures by using custom parameters.
    * Save fits files and return absolute file paths in list type.