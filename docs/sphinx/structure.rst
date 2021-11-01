.. _structure:

Structure
===========

Current fits header
--------------------
.. code-block:: console

    $ clu
    lvmcam expose -p "foo/bar" -r "00h42m44s" -d "41d16m09s" -K 10 -f 1800 0.1 3 sci.agw
    03:32:36.491 lvmcam > 
    03:32:39.825 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/foo/bar/2459519/sci.agw-00000001.fits",
            "1": "/home/mgjeon/lvmcam/foo/bar/2459519/sci.agw-00000002.fits",
            "2": "/home/mgjeon/lvmcam/foo/bar/2459519/sci.agw-00000003.fits"
        }
    }
    03:32:39.828 lvmcam : 
    
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
     - 0.0.301
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
     - 2021-11-01T03:31:20.126
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
     - 5.299259725669739
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
     - 0.268798828125 A
     - Power Supply Current
   * - TOTALDIS
     - 1.7733557224273682 W
     - Total Dissiapted Power
   * - CAMERATE
     - 50.125 C
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
     - 10.68333333333333
     - [deg] RA at reference pixel                    
   * - CRVAL2
     - 41.26916666666666
     - [deg] DEC at reference pixel                   
   * - CD1_1
     - -9.7981553605101E-05
     - [deg/px] WCS matrix diagonal                   
   * - CD2_2
     - 9.79815536051017E-05
     - [deg/px] WCS matrix diagonal                   
   * - CD1_2
     - -0.00026920210605309
     - [deg/px] WCS matrix outer diagonal             
   * - CD2_1
     - -0.00026920210605309
     - [deg/px] WCS matrix outer diagonal 
   * - BSCALE
     - 1
     - 
   * - BZERO
     - 32768
     - 
   * - CHECKSUM
     - WBi9X9g9WAg9W9g9
     - HDU checksum updated 2021-11-01T12:30:45
   * - DATASUM
     - 2464420802
     - data unit checksum updated 2021-11-01T12:30:45


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
| PIXELFOR | sdss/LVM_FLIR_Software    |
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

Current rule of fits file name
--------------------------
.. code-block:: console

    $ clu
    lvmcam expose -p "foo/bar" -r "00h42m44s" -d "41d16m09s" -K 10 -f 1800 0.1 3 sci.agw
    03:32:36.491 lvmcam > 
    03:32:39.825 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/foo/bar/2459519/sci.agw-00000001.fits",
            "1": "/home/mgjeon/lvmcam/foo/bar/2459519/sci.agw-00000002.fits",
            "2": "/home/mgjeon/lvmcam/foo/bar/2459519/sci.agw-00000003.fits"
        }
    }
    03:32:39.828 lvmcam : 

* (FILEPATH from ``-p``)/(Julian day)/``Camera Name-XXXXXXXX.fits``
    * ``-p`` default = ``python/lvmcam/assets``
    * ``XXXXXXXX`` = 8-digit number started from last fits file number

Sequence diagram of lvmcam
--------------------------
This sequence diagram is drawn when EXPTIME = 0.1, 0.5, 1.0, 5.0 second.

.. image:: ./_static/lvmcam_sequence_diagram.png
    :width: 800

