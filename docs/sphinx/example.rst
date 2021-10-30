.. _example:

Example
========

Exposure test with real camera
-------------------------------

Start the actor (in debug mode).

.. code-block:: console

    $ lvmcam start (--debug)

In another terminal, start ``clu``.

.. code-block:: console

    $ clu 

In ``clu`` terminal, type following commands step-by-step.

.. code-block:: console

    $ clu
    lvmcam connect
    12:05:45.900 lvmcam > 
    12:05:50.920 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    12:05:50.931 lvmcam : 
    lvmcam expose -r 10 -d 10 -K 10 0.1 3 sci.agw
    12:06:15.383 lvmcam > 
    12:06:18.801 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/sci.agw-00000001.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/sci.agw-00000002.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/sci.agw-00000003.fits"
        }
    }
    12:06:18.806 lvmcam : 
    lvmcam expose -f "foo/bar" 0.1 3 sci.agw
    12:06:28.633 lvmcam > 
    12:06:32.027 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/foo/bar/2459513/sci.agw-00000004.fits",
            "1": "/home/mgjeon/lvmcam/foo/bar/2459513/sci.agw-00000005.fits",
            "2": "/home/mgjeon/lvmcam/foo/bar/2459513/sci.agw-00000006.fits"
        }
    }
    12:06:32.033 lvmcam :
 

Header (1)
^^^^^^^^^^
The current headers of fits file are as follows.

.. list-table:: 
   :header-rows: 1

   * - Header
     - Value
     - Comment
   * - SIMPLE
     - T
     - conforms to FITS standard
   * - BITPIX
     - 16
     - array data type
   * - NAXIS
     - 2
     - number of array dimensions
   * - NAXIS1
     - 1600
     - 
   * - NAXIS2
     - 1100
     - 
   * - VCAM
     - 0.0.270
     - Version of the camera library
   * - CAMNAME
     - sci.agw
     - Camera name
   * - CAMUID
     - 19283193
     - Camera UID
   * - IMAGETYP
     - object
     - The image type of the file
   * - EXPTIME
     - 0.1
     - Exposure time of single integration [s]
   * - EXPTIMEN
     - 0.1
     - Total exposure time [s]
   * - STACK
     - 1
     - Number of stacked frames
   * - STACKFUN
     - median
     - Function used for stacking
   * - TIMESYS
     - TAI
     - The time scale system
   * - DATE-OBS
     - 2021-09-29T08:38:39.397
     - Date (in TIMESYS) the exposure started
   * - BINX
     - 1
     - [ct] Horizontal Bin Factor 1, 2 or 4
   * - BINY
     - 1
     - [ct] Vertical Bin Factor 1, 2 or 4
   * - WIDTH
     - 1600
     - [ct] Pixel Columns
   * - HEIGHT
     - 1100
     - [ct] Pixel Rows
   * - REGX
     - 1
     - [ct] Pixel Region Horiz start
   * - REGY
     - 1
     - [ct] Pixel Region Vert start
   * - GAIN
     - 17.89790889664172
     - Gain
   * - REVERSEX
     - F
     - Flipped left-right
   * - REVERSEY
     - T
     - Flipped up-down
   * - BINMODEX
     - Sum
     - Horiz Bin Mode Sum or Averag
   * - BINMODEY
     - Sum
     - Vert Bin Mode Sum or Averag
   * - CAMBLCLM
     - F
     - Black Level Clamping en/disabled
   * - CAMTYP
     - Blackfly S BFS-PGE-16S7M
     - Camera model
   * - CRPIX1
     - 800.0
     - [px] RA center along axis 1
   * - CRPIX2
     - -1238.301111111111
     - [px] DEC center along axis 2
   * - PIXELFOR
     - Mono16
     - Pixel format
   * - ROI
     - 1600x1100 at 0,0
     - ROI
   * - FRAMERAT
     - (min=1.0, max=31.46968198249933)
     - Framerate bounds
   * - GAINCONV
     - LCG
     - Gain Conv.
   * - GAMMAENA
     - False
     - Gamma Enable
   * - GAMMAVAL
     - 0.800048828125
     - Gamma Value
   * - ACQUISIT
     - SingleFrame
     - Acquisition mode
   * - EXPTIMEB
     - (min=14.0, max=30000003.0)
     - Exp. time bounds
   * - GAINBOUN
     - (min=0.0, max=47.994294033026364)
     - Gain bounds
   * - POWERSUP
     - 0.1689453125 A
     - Power Supply Current
   * - TOTALDIS
     - 1.873220443725586 W
     - Total Dissiapted Power
   * - CAMERATE
     - 57.75 C
     - Camera Temperature
   * - CUNIT1
     - deg
     - WCS units along axis 1                         
   * - CUNIT2
     - deg
     - WCS units along axis 2                         
   * - CTYPE1
     - RA---TAN
     - WCS type axis 1                                
   * - CTYPE2
     - DEC--TAN
     - WCS type axis 2                                
   * - CRVAL1
     - 10.0
     - [deg] RA at reference pixel                    
   * - CRVAL2
     - 10.0
     - [deg] DEC at reference pixel                   
   * - CD1_1
     - -0.00021469855468581
     - [deg/px] WCS matrix diagonal                   
   * - CD2_2
     - 0.000214698554685812
     - [deg/px] WCS matrix diagonal                   
   * - CD1_2
     - 0.000180153478051160
     - [deg/px] WCS matrix outer diagonal             
   * - CD2_1
     - 0.000180153478051160
     - [deg/px] WCS matrix outer diagonal 
   * - BSCALE
     - 1
     - 
   * - BZERO
     - 32768
     - 
   * - CHECKSUM
     - 9aCDEYBA9aBACWBA
     - HDU checksum updated 2021-09-29T17:38:02 
   * - DATASUM
     - 2128147065
     - data unit checksum updated 2021-09-29T17:38:02 


Header (2)
^^^^^^^^^^
The above headers are created by different source.

+----------+---------------------------+
| Header   | Source                    |
+==========+===========================+
| SIMPLE   | sdss/basecam              |
+----------+                           |
| BITPIX   |                           |
+----------+                           |
| NAXIS    |                           |
+----------+                           |
| NAXIS1   |                           |
+----------+                           |
| NAXIS2   |                           |
+----------+                           |
| VCAM     |                           |
+----------+                           |
| CAMNAME  |                           |
+----------+                           |
| CAMUID   |                           |
+----------+                           |
| IMAGETYP |                           |
+----------+                           |
| EXPTIME  |                           |
+----------+                           |
| EXPTIMEN |                           |
+----------+                           |
| STACK    |                           |
+----------+                           |
| STACKFUN |                           |
+----------+                           |
| TIMESYS  |                           |
+----------+                           |
| DATE-OBS |                           |
+----------+---------------------------+
| BINX     | sdss/araviscam            |
+----------+                           |
| BINY     |                           |
+----------+                           |
| WIDTH    |                           |
+----------+                           |
| HEIGHT   |                           |
+----------+                           |
| REGX     |                           |
+----------+                           |
| REGY     |                           |
+----------+                           |
| GAIN     |                           |
+----------+                           |
| REVERSEX |                           |
+----------+                           |
| REVERSEY |                           |
+----------+                           |
| BINMODEX |                           |
+----------+                           |
| BINMODEY |                           |
+----------+                           |
| CAMBLCLM |                           |
+----------+                           |
| CAMTYP   |                           |
+----------+                           |
| CRPIX1   |                           |
+----------+                           |
| CRPIX2   |                           |
+----------+---------------------------+
| PIXELFOR | FILR library using Aravis |
+----------+                           |
| ROI      |                           |
+----------+                           |
| FRAMERAT |                           |
+----------+                           |
| GAINCOV  |                           |
+----------+                           |
| GAMMAENA |                           |
+----------+                           |
| GAMMAVAL |                           |
+----------+                           |
| ACQUISIT |                           |
+----------+                           |
| EXPTIMEB |                           |
+----------+                           |
| GAINBOUN |                           |
+----------+                           |
| POWERSUP |                           |
+----------+                           |
| TOTALDIS |                           |
+----------+                           |
| CAMERATE |                           |
+----------+---------------------------+
| CUNIT1   | sdss/araviscam            |
+----------+                           |
| CUNIT2   |                           |
+----------+                           |
| CTYPE1   |                           |
+----------+                           |
| CTYPE2   |                           |
+----------+                           |
| CRVAL1   |                           |
+----------+                           |
| CRVAL2   |                           |
+----------+                           |
| CD1_1    |                           |
+----------+                           |
| CD2_2    |                           |
+----------+                           |
| CD1_2    |                           |
+----------+                           |
| CD2_1    |                           |
+----------+---------------------------+
| BSCALE   | sdss/basecam              |
+----------+                           |
| BEZERO   |                           |
+----------+                           |
| CHECKSUM |                           |
+----------+                           |
| DATASUM  |                           |
+----------+---------------------------+

Exposure test with virtual camera
----------------------------------

Start the actor (in debug mode).

.. code-block:: console

   $ lvmcam start (--debug)

In another terminal, start ``clu``.

.. code-block:: console

   $ clu 

In ``clu`` terminal, type following commands step-by-step. The ``--test`` or ``-t`` option in ``connect`` command makes a 'test' camera.

.. code-block:: console

    $ clu
    lvmcam connect -t
    12:08:17.298 lvmcam > 
    12:08:17.299 lvmcam i {
        "CAMERA": {
            "name": "test",
            "uid": "-1"
        }
    }
    12:08:17.300 lvmcam : 
    lvmcam expose 0.1 3 test
    12:08:25.268 lvmcam > 
    12:08:25.590 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/test-00000001.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/test-00000002.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459513/test-00000003.fits"
        }
    }
    12:08:25.595 lvmcam : 
    

The 'test' camera is fake camera. All images captured by the 'test' camera are just files copied from `python/lvmcam/actor/example`.


Test shot
---------  

The ``--testshot`` or ``-t`` option in ``expose`` command makes one ``test.fits`` file that is always overwritten. 
The ``NUM`` argument of ``expose`` is ignored.

.. code-block:: console

    $ clu
    lvmcam connect -t
    12:11:50.442 lvmcam > 
    12:11:50.443 lvmcam i {
        "CAMERA": {
            "name": "test",
            "uid": "-1"
        }
    }
    12:11:50.444 lvmcam : 
    lvmcam expose -t 0.1 3 test
    12:11:57.167 lvmcam > 
    12:11:57.273 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/test.fits"
        }
    }
    12:11:57.274 lvmcam : 
    lvmcam disconnect
    12:12:00.238 lvmcam > 
    12:12:00.239 lvmcam i {
        "text": "Cameras have been removed"
    }
    12:12:00.240 lvmcam : 
    lvmcam connect
    12:12:04.067 lvmcam > 
    12:12:09.091 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    12:12:09.101 lvmcam : 
    lvmcam expose -t 0.1 3 sci.agw
    12:12:15.066 lvmcam > 
    12:12:17.406 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/test.fits"
        }
    }
    12:12:17.412 lvmcam : 
 


Show commands
--------------

The 'Available' means that the camera can be connected.

.. code-block:: console

    $ clu
    lvmcam show all
    12:12:49.081 lvmcam > 
    12:12:51.425 lvmcam i {
        "ALL": {
            "sci.agw": "Available",
            "sci.age": "Unavailable",
            "sci.agc": "Unavailable",
            "skyw.agw": "Unavailable",
            "skyw.age": "Unavailable",
            "skyw.agc": "Unavailable",
            "skye.agw": "Unavailable",
            "skye.age": "Unavailable",
            "skye.agc": "Unavailable",
            "spec.agw": "Unavailable",
            "spec.age": "Unavailable",
            "spec.agc": "Unavailable"
        }
    }
    12:12:51.430 lvmcam : 
    
 

``lvmcam show connection`` shows all connected cameras. This reply is similar to that of ``lvmcam connect``.

.. code-block:: console

    $ clu
    lvmcam show connection
    12:13:44.881 lvmcam > 
    12:13:44.937 lvmcam e {
        "text": "There are no connected cameras"
    }
    lvmcam connect -t
    12:13:50.888 lvmcam > 
    12:13:50.889 lvmcam i {
        "CAMERA": {
            "name": "test",
            "uid": "-1"
        }
    }
    12:13:50.890 lvmcam : 
    lvmcam show connection
    12:13:55.143 lvmcam > 
    12:13:55.203 lvmcam i {
        "CONNECTED": {
            "name": "test",
            "uid": "-1"
        }
    }
    12:13:55.204 lvmcam : 
    lvmcam connect
    12:13:58.360 lvmcam > 
    12:13:58.362 lvmcam e {
        "text": "Cameras are already connected"
    }
    lvmcam disconnect
    12:14:01.035 lvmcam > 
    12:14:01.036 lvmcam i {
        "text": "Cameras have been removed"
    }
    12:14:01.037 lvmcam : 
    lvmcam connect
    12:14:04.052 lvmcam > 
    12:14:09.075 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    12:14:09.083 lvmcam : 
    lvmcam show connection
    12:14:12.393 lvmcam > 
    12:14:12.465 lvmcam i {
        "CONNECTED": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    12:14:12.466 lvmcam : 
    

Status command
--------------

.. code-block:: console

    $ clu
    lvmcam status
    12:14:48.884 lvmcam > 
    12:14:51.161 lvmcam i {
        "STATUS": {
            "Camera model": "Blackfly S BFS-PGE-16S7M",
            "Camera vendor": "FLIR",
            "Camera id": "19283193",
            "Pixel format": "Mono16",
            "Available Formats": "['Mono8', 'Mono16', 'Mono10Packed', 'Mono12Packed', 'Mono10p', 'Mono12p']",
            "Full Frame": "1608x1104",
            "ROI": "1600x1100 at 0,0",
            "Frame size": "3520000 Bytes",
            "Frame rate": "27.695798215061195 Hz",
            "Exposure time": "0.099996 seconds",
            "Gain Conv.": "LCG",
            "Gamma Enable": "False",
            "Gamma Value": "0.800048828125",
            "Acquisition mode": "SingleFrame",
            "Framerate bounds": "(min=1.0, max=31.46968198249933)",
            "Exp. time bounds": "(min=14.0, max=30000003.0)",
            "Gain bounds": "(min=0.0, max=47.994294033026364)",
            "Power Supply Voltage": "9.76171875 V",
            "Power Supply Current": "0.259765625 A",
            "Total Dissiapted Power": "2.569320797920227 W",
            "Camera Temperature": "55.25 C"
        }
    }
    12:14:51.166 lvmcam : 
    