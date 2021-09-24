# Changelog

## 0.1.2 - September 24, 2021

### 🔧 Fixed

* Fixed `PermissionError: [Errno 13] Permission denied: '/python'` error that occurs when `lvmcam start` runs without `--debug` option.


## 0.1.1 - September 13, 2021

### 🚀 New

* Added options for test.
    * `lvmcam connect --test`: add virtual camera
    * `expose --testshot EXPTIME NUM CAMNAME`: Test shot

## 0.1.0 - September 6, 2021

### 🚀 New

* Initial version of lvmcam.
* Basic features.
    * Show status of cameras.
    * Connect/Disconnect cameras.
    * Take exposure pictures by using custom parameters.
    * Save fits files and return absolute file paths in list type.