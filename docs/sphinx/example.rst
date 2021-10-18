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
    06:54:23.681 lvmcam > 
    06:54:28.691 lvmcam i {
        "text": "{'name': sci.agw, 'uid': 19283193}"
    }
    06:54:28.700 lvmcam : 
    lvmcam expose -r 10 -d 10 -K 10 0.1 3 sci.agw
    06:55:00.238 lvmcam > 
    06:55:03.647 lvmcam i {
        "text": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459505/sci.agw-00000001.fits"
    }
    06:55:03.652 lvmcam i {
        "text": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459505/sci.agw-00000002.fits"
    }
    06:55:03.653 lvmcam i {
        "text": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459505/sci.agw-00000003.fits"
    }
    06:55:03.654 lvmcam : 
 


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
    lvmcam connect -t
    06:56:22.722 lvmcam > 
    06:56:22.724 lvmcam i {
        "text": "{'name': test, 'uid': -1}"
    }
    06:56:22.725 lvmcam : 
    lvmcam expose 0.1 3 test
    06:56:32.869 lvmcam > 
    06:56:33.191 lvmcam i {
        "text": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459505/test-00000001.fits"
    }
    06:56:33.196 lvmcam i {
        "text": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459505/test-00000002.fits"
    }
    06:56:33.197 lvmcam i {
        "text": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459505/test-00000003.fits"
    }
    06:56:33.198 lvmcam : 
    


The 'test' camera is just fake camera. All images gotten by test camera are files copied of `python/lvmcam/actor/example`.


Test shot
---------  

The ``--testshot`` option in ``expose`` command makes one ``test.fits`` file that is always overwritten. 
The ``NUM`` argument of ``expose`` is ignored.

.. code-block:: console

    $ clu
    lvmcam expose -t 0.1 3 sci.agw
    06:58:11.853 lvmcam > 
    06:58:14.174 lvmcam i {
        "text": "/home/mgjeon/lvmcam/python/lvmcam/assets/test.fits"
    }
    06:58:14.180 lvmcam : 


Show commands
--------------

The 'available' means that the camera can be connected.

.. code-block:: console

    $ clu
    lvmcam show all
    06:58:54.787 lvmcam > 
    06:58:57.122 lvmcam i {
        "text": "available: ('sci.agw', {'name': 'sci.agw', 'uid': '19283193', 'serial': 19283193, 'ip': '192.168.70.50', 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283193', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': True, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.127 lvmcam i {
        "text": "unavailable: ('sci.age', {'name': 'sci.age', 'uid': '19283182', 'serial': 19283182, 'ip': '192.168.70.70', 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283182', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': True, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.128 lvmcam i {
        "text": "unavailable: ('sci.agc', {'name': 'sci.agc', 'uid': '-100', 'serial': 0, 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283186', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': False, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.129 lvmcam i {
        "text": "unavailable: ('skyw.agw', {'name': 'skyw.agw', 'uid': '-2', 'serial': 0, 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283186', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': True, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.130 lvmcam i {
        "text": "unavailable: ('skyw.age', {'name': 'skyw.age', 'uid': '-3', 'serial': 0, 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283186', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': True, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.131 lvmcam i {
        "text": "unavailable: ('skyw.agc', {'name': 'skyw.agc', 'uid': '-101', 'serial': 0, 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283186', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': False, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.132 lvmcam i {
        "text": "unavailable: ('skye.agw', {'name': 'skye.agw', 'uid': '-4', 'serial': 0, 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283186', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': True, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.133 lvmcam i {
        "text": "unavailable: ('skye.age', {'name': 'skye.age', 'uid': '-5', 'serial': 0, 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283186', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': True, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.134 lvmcam i {
        "text": "unavailable: ('skye.agc', {'name': 'skye.agc', 'uid': '-102', 'serial': 0, 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283186', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': False, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.135 lvmcam i {
        "text": "unavailable: ('spec.agw', {'name': 'spec.agw', 'uid': '-6', 'serial': 0, 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283186', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': False, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.136 lvmcam i {
        "text": "unavailable: ('spec.age', {'name': 'spec.age', 'uid': '-7', 'serial': 0})"
    }
    06:58:57.137 lvmcam i {
        "text": "unavailable: ('spec.agc', {'name': 'spec.agc', 'uid': '-103', 'serial': 0, 'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283186', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 'bool': {'ReverseY': True, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False})"
    }
    06:58:57.138 lvmcam : 
 

``lvmcam show connection`` shows all connected cameras. This reply is equal to that of lvmcam connect.

.. code-block:: console

    $ clu
    lvmcam show connection
    07:01:44.699 lvmcam > 
    07:01:44.750 lvmcam e {
        "text": "There are no connected cameras"
    }
    lvmcam connect -t
    07:01:51.030 lvmcam > 
    07:01:51.031 lvmcam i {
        "text": "{'name': test, 'uid': -1}"
    }
    07:01:51.032 lvmcam : 
    lvmcam show connection
    07:01:55.295 lvmcam > 
    07:01:55.354 lvmcam i {
        "text": "{ 'name': test, 'uid': -1 }"
    }
    07:01:55.355 lvmcam : 
    lvmcam connect
    07:01:58.131 lvmcam > 
    07:02:03.125 lvmcam i {
        "text": "{'name': test, 'uid': -1}"
    }
    07:02:03.134 lvmcam i {
        "text": "{'name': sci.agw, 'uid': 19283193}"
    }
    07:02:03.135 lvmcam : 
    lvmcam show connection
    07:02:06.885 lvmcam > 
    07:02:06.964 lvmcam i {
        "text": "{ 'name': test, 'uid': -1 }"
    }
    07:02:06.965 lvmcam i {
        "text": "{ 'name': sci.agw, 'uid': 19283193 }"
    }
    07:02:06.966 lvmcam : 
    

Status command
--------------

.. code-block:: console

    $ clu
    lvmcam status
    07:03:39.788 lvmcam > 
    07:03:42.061 lvmcam i {
        "text": "Camera model: Blackfly S BFS-PGE-16S7M"
    }
    07:03:42.066 lvmcam i {
        "text": "Camera vendor: FLIR"
    }
    07:03:42.067 lvmcam i {
        "text": "Camera id: 19283193"
    }
    07:03:42.068 lvmcam i {
        "text": "Pixel format: Mono16"
    }
    07:03:42.069 lvmcam i {
        "text": "Available Formats: ['Mono8', 'Mono16', 'Mono10Packed', 'Mono12Packed', 'Mono10p', 'Mono12p']"
    }
    07:03:42.070 lvmcam i {
        "text": "Full Frame: 1608x1104"
    }
    07:03:42.071 lvmcam i {
        "text": "ROI: 1600x1100 at 0,0"
    }
    07:03:42.072 lvmcam i {
        "text": "Frame size: 3520000 Bytes"
    }
    07:03:42.073 lvmcam i {
        "text": "Frame rate: 27.695798215061195 Hz"
    }
    07:03:42.074 lvmcam i {
        "text": "Exposure time: 0.099996 seconds"
    }
    07:03:42.075 lvmcam i {
        "text": "Gain Conv.: LCG"
    }
    07:03:42.076 lvmcam i {
        "text": "Gamma Enable: False"
    }
    07:03:42.077 lvmcam i {
        "text": "Gamma Value: 0.800048828125"
    }
    07:03:42.079 lvmcam i {
        "text": "Acquisition mode: SingleFrame"
    }
    07:03:42.084 lvmcam i {
        "text": "Framerate bounds: (min=1.0, max=31.46968198249933)"
    }
    07:03:42.085 lvmcam i {
        "text": "Exp. time bounds: (min=14.0, max=30000003.0)"
    }
    07:03:42.086 lvmcam i {
        "text": "Gain bounds: (min=0.0, max=47.994294033026364)"
    }
    07:03:42.087 lvmcam i {
        "text": "Power Supply Voltage: 9.73681640625 V"
    }
    07:03:42.088 lvmcam i {
        "text": "Power Supply Current: 0.18994140625 A"
    }
    07:03:42.090 lvmcam i {
        "text": "Total Dissiapted Power: 2.0348424911499023 W"
    }
    07:03:42.092 lvmcam i {
        "text": "Camera Temperature: 56.25 C"
    }
    07:03:42.092 lvmcam : 
