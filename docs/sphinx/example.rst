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
   lvmcam expose 0.1 3 sci.agw
   02:36:06.480 lvmcam > 
   02:36:09.742 lvmcam : {
      "path": [
         "/home/mgjeon/lvmcam/python/lvmcam/assets/2459471/sci.agw-00000001.fits",
         "/home/mgjeon/lvmcam/python/lvmcam/assets/2459471/sci.agw-00000002.fits",
         "/home/mgjeon/lvmcam/python/lvmcam/assets/2459471/sci.agw-00000003.fits"
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
     - True
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
     - 0.0.138
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
     - 2021-09-14T02:36:44.719
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
     - 4.199427234238525
     - Gain
   * - REVERSEX
     - False
     - Flipped left-right
   * - REVERSEY
     - True
     - Flipped up-down
   * - BINMODEX
     - Sum
     - Horiz Bin Mode Sum or Averag
   * - BINMODEY
     - Sum
     - Vert Bin Mode Sum or Averag
   * - CAMBLCLM
     - False
     - Black Level Clamping en/disabled
   * - CAMTYP
     - Blackfly S BFS-PGE-16S7M
     - Camera model
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
     - 0.228515625 A
     - Power Supply Current
   * - TOTALDIS
     - 2.045455574989319 W
     - Total Dissiapted Power
   * - CAMERATE
     - 59.625 C
     - Camera Temperature
   * - BSCALE
     - 1
     - 
   * - BZERO
     - 32768
     - 
   * - CHECKSUM
     - RYefSWdcRWdcRWdc
     - HDU checksum updated 2021-09-14T11:36:09
   * - DATASUM
     - 3015725399
     - data unit checksum updated 2021-09-14T11:36:09


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
| BSCALE   | sdss/basecam              |
+----------+                           |
| BEZERO   |                           |
+----------+                           |
| CHECKSUM |                           |
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
   