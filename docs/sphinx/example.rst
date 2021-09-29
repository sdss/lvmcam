.. _example:

Example
========

Exposure test with real camera
-------------------------------

Start the actor in debug mode.

.. code-block:: console

   $ lvmcam start --debug

In another terminal, start ``clu``.

.. code-block:: console

   $ clu 

In ``clu`` terminal, type following commands step-by-step.

.. code-block:: console

   $ clu
   lvmcam connect
   02:34:51.307 lvmcam > 
   02:34:56.247 lvmcam i {
      "connect": {
         "name": "sci.agw",
         "uid": "19283193"
      }
   }
   lvmcam expose 0.1 3 sci.agw -r 10 -d 10 -K 10
   02:36:06.480 lvmcam > 
   02:36:09.742 lvmcam : {
      "path": [
         "/home/mgjeon/lvmcam/python/lvmcam/assets/2459486/sci.agw-00000001.fits",
         "/home/mgjeon/lvmcam/python/lvmcam/assets/2459486/sci.agw-00000002.fits",
         "/home/mgjeon/lvmcam/python/lvmcam/assets/2459486/sci.agw-00000003.fits"
      ]
   }

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

Start the actor in debug mode.

.. code-block:: console

   $ lvmcam start --debug

In another terminal, start ``clu``.

.. code-block:: console

   $ clu 

In ``clu`` terminal, type following commands step-by-step.

.. code-block:: console

   $ clu
   lvmcam connect --test
   03:32:51.938 lvmcam > 
   03:32:51.945 lvmcam i {
      "connect": {
         "name": "test",
         "uid": "-1"
      }
   }
   lvmcam expose 0.1 3 test
   03:33:02.412 lvmcam > 
   03:33:02.427 lvmcam : {
      "path": [
         "/home/mgjeon/lvmcam/python/lvmcam/assets/2459471/test-00000001.fits",
         "/home/mgjeon/lvmcam/python/lvmcam/assets/2459471/test-00000002.fits",
         "/home/mgjeon/lvmcam/python/lvmcam/assets/2459471/test-00000003.fits"
      ]
   }

The 'test' camera is just fake camera. All images gotten by test camera are files copied of `python/lvmcam/actor/example`.


Test shot
---------  

The ``--testshot`` option in ``expose`` command makes one ``test.fits`` file that is always overwritten. 
The ``NUM`` argument of ``expose`` is ignored.

.. code-block:: console

   lvmcam expose --testshot 0.1 3 sci.agw
   03:43:54.081 lvmcam > 
   03:43:55.886 lvmcam : {
      "path": [
         "/home/mgjeon/lvmcam/python/lvmcam/assets/test.fits"
      ]
   }
   