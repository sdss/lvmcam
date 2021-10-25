# Changelog

## 0.2.0 - October 25, 2021

### 🚀 New
* Restore returned values of actor commands similar to before 0.1.0 version.
    * Add JSON schema

### ✨ Improved
* Change unit testing code so that JSONActor is not used.

## 0.1.0 - October 11, 2021

### 🚀 New
* Change returned values of actor commands because of update of [sdss-clu 1.3.0](https://clu.readthedocs.io/en/latest/changelog.html#september-17-2021)

### ✨ Improved
* Code Refactoring
 
## 0.0.5 - October 5, 2021

### ✨ Improved
* First unit testing
* Delete unnecessary directories and files(filr/*, comutest/) in python/lvmcam/

## 0.0.4 - September 29, 2021

### 🚀 New
* Reflect update of sdss/araviscam on Sep 28, 2021.
    * Add properties such as pixsize and pixcal in cameras.yaml
    * Add headers such as CRPIX1, CRPIX2, CUNIT1, CUNIT2, CTYPE1, CTYPE2, CRVAL1, CRVAL2, CD1_1, CD2_2, CD1_2, and CD2_1.
    * Add options in `lvmcam expose` such as `-r`, `-d`, `-K`. This options are respectively RA J2000 (deg), Dec J2000 (deg), and K-mirror angle (deg).
* Rename versions.

## 0.0.3 - September 24, 2021

### 🔧 Fixed

* Fix errors that occurs when `lvmcam start` runs without `--debug` option.


## 0.0.2 - September 13, 2021

### 🚀 New

* Add options for test.
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