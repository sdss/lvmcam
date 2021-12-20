.. _example:

Example
========

Exposure test with real camera
-------------------------------

Set ``araviscam: True`` in ``python/lvmcam/etc/camtype.yaml``. The path where the images are saved can be changed in ``python/lvmcam/etc/cameras.yaml``.

.. code-block:: console

    camtype:
        araviscam: True
        skymakercam: False


Start the actor (in debug mode).

.. code-block:: console

    $ lvmcam start (--debug)

In another terminal, start ``clu``.

.. code-block:: console

    $ clu 

In ``clu`` terminal, type following commands step-by-step.

.. code-block:: console

    $ clu
    lvmcam connect -v
    00:34:52.026 lvmcam > 
    00:34:56.271 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    00:34:56.282 lvmcam : 
    lvmcam expose -v -r 00h42m44s -d 41d16m09s -K 10 -f 1800 0.1 3 sci.agw
    00:35:15.462 lvmcam > 
    00:35:17.716 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000001.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000002.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000003.fits"
        }
    }
    lvmcam expose -v -r 00h42m44s -d 41d16m09s -K 10 -f 1800 1 3 sci.agw
    00:35:22.831 lvmcam > 
    00:35:27.655 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000004.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000005.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000006.fits"
        }
    }
 

In ``lvmcam start --debug`` terminal, you can see verbosity.

.. code-block:: console

    $ lvmcam start --debug
    [DEBUG]: [1.307 s]: find_all_available_cameras
    [DEBUG]: [1.640 s]: async _connect_internal
    [DEBUG]: [1.641 s]: async connect_available_camera
    [DEBUG]: [1.253 s]: get_cam_dev_for_header
    [DEBUG]: [0.599 s]: async _expose_internal
    [DEBUG]: [0.596 s]: async _expose_internal
    [DEBUG]: [0.595 s]: async _expose_internal
    [DEBUG]: [2.234 s]: async expose_real_cam
    [DEBUG]: [1.499 s]: async _expose_internal
    [DEBUG]: [1.496 s]: async _expose_internal
    [DEBUG]: [1.495 s]: async _expose_internal
    [DEBUG]: [4.821 s]: async expose_real_cam




Exposure test with virtual camera
----------------------------------

Set ``askymakercam: True`` in ``python/lvmcam/etc/camtype.yaml``. The path where the images are saved can be changed in ``python/lvmcam/etc/cameras.yaml``.

.. code-block:: console

    camtype:
        araviscam: False
        skymakercam: True

Start `lvmtan <https://github.com/sdss/lvmtan>`_, `lvmpwi <https://github.com/sdss/lvmpwi>`_, and `skymakercam <https://github.com/sdss/skymakercam>`_ as follows.

For lvmtan:

.. code-block:: console

    $ git clone https://github.com/sdss/lvmtan
    $ cd lvmtan
    $ poetry install
    $ poetry run container_start --name=lvm.all


For lvmpwi:

.. code-block:: console

    $ git clone https://github.com/sdss/lvmpwi
    $ cd lvmpwi
    $ poetry install
    $ poetry run container_start --name=lvm.sci.pwi --simulator

For skymakercam:

.. code-block:: console

    $ git clone https://github.com/sdss/skymakercam
    $ cd skymakercam
    $ poetry install
    $ poetry run python utils/plot_skymakercam.py -v -c python/skymakercam/etc/cameras.yaml lvm.sci.agw.cam

Start the actor (in debug mode).

.. code-block:: console

   $ lvmcam start (--debug)

In another terminal, start ``clu``.

.. code-block:: console

   $ clu 

In ``clu`` terminal, type following commands step-by-step.

.. code-block:: console

    $ clu
    lvmcam connect -v
    10:07:35.459 lvmcam >
    10:07:36.592 lvmcam i {
        "CAMERA": {
            "name": "lvm.sci.agw.cam",
            "uid": "lvm.sci.agw.cam"
        }
    }
    10:07:36.603 lvmcam :
    lvmcam expose -v -r 00h42m44s -d 41d16m09s -K 10 -f 1800 0.1 3 lvm.sci.agw.cam
    10:07:52.756 lvmcam >
    10:07:57.813 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211214/lvm.lvm.sci.agw.cam-00000001.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211214/lvm.lvm.sci.agw.cam-00000002.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211214/lvm.lvm.sci.agw.cam-00000003.fits"
        }
    }
    lvmcam expose -v -r 00h42m44s -d 41d16m09s -K 10 -f 1800 1 3 lvm.sci.agw.cam
    10:08:03.555 lvmcam >
    10:08:04.503 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211214/lvm.lvm.sci.agw.cam-00000004.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211214/lvm.lvm.sci.agw.cam-00000005.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211214/lvm.lvm.sci.agw.cam-00000006.fits"
        }
    }


In ``lvmcam start --debug`` terminal, you can see verbosity.


.. code-block:: console

    $ lvmcam start --debug
    [DEBUG]: [SKYCAMERASYSTEM]: read configuration file from /home/mgjeon/lvmcam/python/lvmcam/etc/cameras.yaml
    [DEBUG]: [0.033 s]: find_all_available_cameras
    [DEBUG]: [SKYCAMERASYSTEM]: adding camera 'lvm.sci.agw.cam' with parameters {'type': 'skymakercam', 'uid': 'lvm.sci.agw.cam', 
    'descr': 'Guider Camera Science', 'default': {'gain': 5.0, 'binning': [4, 4]}, 'instpar': 'lvm_sci_agw_cam', 
    'focus_stage': 'lvm.sci.foc', 'kmirror': 'lvm.sci.km', 'tcs': 'lvm.sci.pwi', 'catalog_path': '$HOME/data/catalog/gaia', 
    'pixsize': 9.0, 'pixscal': 8.92, 'connection': {'uid': '19283193', 'gain': 1.0, 'binning': [1, 1], 'autoconnect': True, 
    'bool': {'ReverseY': True, 'ReverseX': False, 'BlackLevelClampingEnable': False, 'GammaEnable': False}, 
    'int': {'BinningHorizontalMode': 1, 'BinningVerticalMode': 1}, 'float': None, 'string': None}, 'shutter': False, 
    'extrahdr': [['TEST1', 9999, 'Extra header test 1'], ['TEST2', 999, 'Extra header test 2'], ['TESTHDR3', -1, 'Extra header test 3'], 
    ['TESTHDR4', -2, 'Extra header test 4']], 'path': {'basename': 'lvm.{camera.name}-{num:08d}.fits', 
    'dirname': "test/{date.strftime('%Y%m%d')}", 'filepath': 'python/lvmcam/assets'}}
    [DEBUG]: [LVM.SCI.AGW.CAM]: [1600, 1100]
    [DEBUG]: [LVM.SCI.AGW.CAM]: connecting ...
    [DEBUG]: [LVM.SCI.AGW.CAM]: camera connected.
    [DEBUG]: [0.048 s]: async connect_available_camera
    [DEBUG]: [LVM.SCI.AGW.CAM]: defocus 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: kmirror angle (deg): 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: separation 6.068631324108885
    Gaia query:  SELECT source_id, ra,dec,phot_g_mean_mag FROM gaiaedr3.gaia_source WHERE phot_g_mean_mag <= 17 AND 1=CONTAINS(POINT('ICRS',ra,dec), 
    CIRCLE('ICRS',48.198614693649,-58.535399463189, 0.692887394120578))
    INFO: Query finished. [astroquery.utils.tap.core]
    1163 stars found within 0.692887394120578 deg
    [DEBUG]: [LVM.SCI.AGW.CAM]: defocus 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: kmirror angle (deg): 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: separation 1.5447622919059536
    [DEBUG]: [LVM.SCI.AGW.CAM]: defocus 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: kmirror angle (deg): 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: separation 1.6575005324400047
    [DEBUG]: [5.046 s]: async expose_cam
    [DEBUG]: [LVM.SCI.AGW.CAM]: defocus 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: kmirror angle (deg): 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: separation 3.82851967502365
    [DEBUG]: [LVM.SCI.AGW.CAM]: defocus 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: kmirror angle (deg): 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: separation 3.9465993299925985
    [DEBUG]: [LVM.SCI.AGW.CAM]: defocus 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: kmirror angle (deg): 0.0
    [DEBUG]: [LVM.SCI.AGW.CAM]: separation 4.062583024766025
    [DEBUG]: [0.954 s]: async expose_cam



Test shot
---------  

The ``--testshot`` or ``-t`` option in ``expose`` command makes one ``testshot.fits`` file that is always overwritten. 
The ``NUM`` argument of ``expose`` is ignored.

.. code-block:: console

    $ clu
    lvmcam connect
    10:14:07.696 lvmcam >
    10:14:08.828 lvmcam i {
        "CAMERA": {
            "name": "lvm.sci.agw.cam",
            "uid": "lvm.sci.agw.cam"
        }
    }
    10:14:08.842 lvmcam :
    lvmcam expose -t 0.1 3 lvm.sci.agw.cam
    10:14:15.496 lvmcam >
    10:14:19.892 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/testshot.fits"
        }
    }
    lvmcam connect
    10:14:26.887 lvmcam >
    10:14:26.888 lvmcam e {
        "error": "Cameras are already connected"
    }
    10:14:26.890 lvmcam f
    lvmcam disconnect
    10:14:29.898 lvmcam >
    10:14:29.899 lvmcam i {
        "text": "Cameras have been removed"
    }
    10:14:29.901 lvmcam :
    
 


Show commands
--------------

The 'Available' means that the camera can be connected.

.. code-block:: console

    $ clu
    lvmcam show all
    10:14:55.454 lvmcam >
    10:14:55.491 lvmcam i {
        "ALL": {
            "lvm.sci.agw.cam": "Available | uid: lvm.sci.agw.cam",
            "sci.agw": "Unavailable | uid: 19283193",
            "sci.age": "Unavailable | uid: 19283182",
            "sci.agc": "Unavailable | uid: -100",
            "skyw.agw": "Unavailable | uid: -2",
            "skyw.age": "Unavailable | uid: -3",
            "skyw.agc": "Unavailable | uid: -101",
            "skye.agw": "Unavailable | uid: -4",
            "skye.age": "Unavailable | uid: -5",
            "skye.agc": "Unavailable | uid: -102",
            "spec.agw": "Unavailable | uid: -6",
            "spec.age": "Unavailable | uid: -7",
            "spec.agc": "Unavailable | uid: -103"
        }
    }
    10:14:55.507 lvmcam :
 
 

``lvmcam show connection`` shows all connected cameras. This reply is similar to that of ``lvmcam connect``.

.. code-block:: console

    $ clu
    lvmcam show connection
    10:15:19.205 lvmcam >
    10:15:19.206 lvmcam e {
        "error": "There are no connected cameras"
    }
    10:15:19.207 lvmcam f
    lvmcam connect
    10:15:24.475 lvmcam >
    10:15:25.614 lvmcam i {
        "CAMERA": {
            "name": "lvm.sci.agw.cam",
            "uid": "lvm.sci.agw.cam"
        }
    }
    10:15:25.624 lvmcam :
    lvmcam show connection
    10:15:28.656 lvmcam >
    10:15:28.657 lvmcam i {
        "CONNECTED": {
            "name": "lvm.sci.agw.cam",
            "uid": "lvm.sci.agw.cam"
        }
    }
    10:15:28.658 lvmcam :
 

Status command
--------------

.. code-block:: console

    $ clu
    lvmcam status
    00:30:46.707 lvmcam > 
    00:30:48.080 lvmcam i {
        "STATUS": {
            "Camera model": "Blackfly S BFS-PGE-16S7M",
            "Camera vendor": "FLIR",
            "Camera id": "19283193",
            "Pixel format": "Mono16",
            "Available Formats": "['Mono8', 'Mono16', 'Mono10Packed', 'Mono12Packed', 'Mono10p', 'Mono12p']",
            "Full Frame": "1608x1104",
            "ROI": "1600x1100 at 0,0",
            "Frame size": "3520000 Bytes",
            "Frame rate": "3.392067663337556 Hz",
            "Exposure time": "0.999999 seconds",
            "Gain Conv.": "LCG",
            "Gamma Enable": "False",
            "Gamma Value": "0.800048828125",
            "Acquisition mode": "SingleFrame",
            "Framerate bounds": "(min=1.0, max=3.3953648380635064)",
            "Exp. time bounds": "(min=14.0, max=30000003.0)",
            "Gain bounds": "(min=0.0, max=47.994294033026364)",
            "Power Supply Voltage": "9.76171875 V",
            "Power Supply Current": "0.28369140625 A",
            "Total Dissiapted Power": "2.716955542564392 W",
            "Camera Temperature": "33.5 C"
        }
    }
    00:30:48.088 lvmcam : 
 

Extra header
------------
You can add an extra header in result fits file.


1. Using ``--header`` or ``-h`` option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``--header`` option is passed 'JSON header' similar to `archon <https://github.com/sdss/archon/blob/c28080d145072dc80dedff111d6d589a7fd195ff/archon/actor/commands/expose.py#L145>`_. The rule for 'JSON header' is ``{Header1: (Value1, Comment1), Header2: (Value2, Comment2) ...}``.


.. code-block:: console

    $ clu
    lvmcam expose 0.1 1 sci.agw --header '{"HDRTEST1": (8888, "extra hdr TEST 1"), "HDRTEST2": ("test value", "test comment"), "HDRTEST3": (-8, "extra hdr test 3")}'
    04:55:22.919 lvmcam > 
    04:55:23.617 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211212/lvm.sci.agw-00000001.fits"
        }


.. code-block:: console

    SIMPLE  =                    T / conforms to FITS standard                      
    BITPIX  =                   16 / array data type                                
    NAXIS   =                    3 / number of array dimensions                     
    NAXIS1  =                 1600                                                  
    NAXIS2  =                 1100                                                  
    NAXIS3  =                    1                                                  
    EXTEND  =                    T                                                  
    BSCALE  =                    1                                                  
    BZERO   =                32768                                                  
    CAMNAME = 'sci.agw '           / Camera name                                    
    CAMUID  =             19283193 / Camera UID                                     
    IMAGETYP= 'object  '           / The image type of the file                     
    EXPTIME =                  0.1 / Exposure time of single integration [s]        
    DATE-OBS= '2021-12-12T04:55:59.912' / Date (in TIMESYS) the exposure started    
    PXFORMAT= 'Mono16  '           / Pixel format                                   
    FULLFRAM= '1608x1104'          / Full Frame                                     
    ROI     = '1600x1100 at 0,0'   / ROI                                            
    FRAMSIZE=              3520000 / Frame size (Bytes)                             
    FRAMRATE=    3.392067663337556 / Frame rate (Hz)                                
    EXPTIME =             0.099996 / Exposure time (seconds)                        
    GAINCONV= 'LCG     '           / Gain Conv.                                     
    GAMMAENA=                    F / Gamma Enable                                   
    GAMMAVAL=       0.800048828125 / Gamma Value                                    
    ACQUIMOD= 'SingleFrame'        / Acquisition mode                               
    FRMRATBD= '(min=1.0, max=3.3953648380635064)' / Framerate bounds                
    EXPTIMBD= '(min=14.0, max=30000003.0)' / Exp. time bounds                       
    GAINBD  = '(min=0.0, max=47.994294033026364)' / Gain bounds                     
    VOLTAGE =         9.7451171875 / Power Supply Voltage (V)                       
    CURRENT =        0.18115234375 / Power Supply Current (A)                       
    POWER   =     1.23955225944519 / Total Dissiapted Power (W)                     
    CAMTEMP =                 38.5 / Camera Temperature (C)                         
    HDRTEST1=                 8888 / extra hdr TEST 1                               
    HDRTEST2= 'test value'         / test comment                                   
    HDRTEST3=                   -8 / extra hdr test 3                               
    CHECKSUM= 'ZXnDcUl9ZUlCbUl9'   / HDU checksum updated 2021-12-12T13:55:23       
    DATASUM = '2816880889'         / data unit checksum updated 2021-12-12T13:55:23 
    END                                                                             



2. Using ``--extraheader`` or ``-eh`` option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``--extraheader`` option allows extrahdr in cameras.yaml to be added.

.. code-block:: console
  
  # cameras.yaml
  cameras:
    sci.agw:
      name: "sci.agw"
      ...
      extrahdr: [
         ['TEST1',               9999, "Extra header test 1"],
         ['TEST2',                999, "Extra header test 2"],
         ['TESTHDR3',    -1, "Extra header test 3"],
         ['TESTHDR4',    -2, "Extra header test 4"]
        ]


.. code-block:: console

    $ clu
    lvmcam expose 0.1 1 sci.agw --extraheader
    04:57:15.148 lvmcam > 
    04:57:15.850 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211212/lvm.sci.agw-00000002.fits"
        }


.. code-block:: console

    SIMPLE  =                    T / conforms to FITS standard                      
    BITPIX  =                   16 / array data type                                
    NAXIS   =                    3 / number of array dimensions                     
    NAXIS1  =                 1600                                                  
    NAXIS2  =                 1100                                                  
    NAXIS3  =                    1                                                  
    EXTEND  =                    T                                                  
    BSCALE  =                    1                                                  
    BZERO   =                32768                                                  
    CAMNAME = 'sci.agw '           / Camera name                                    
    CAMUID  =             19283193 / Camera UID                                     
    IMAGETYP= 'object  '           / The image type of the file                     
    EXPTIME =                  0.1 / Exposure time of single integration [s]        
    DATE-OBS= '2021-12-12T04:57:52.146' / Date (in TIMESYS) the exposure started    
    PXFORMAT= 'Mono16  '           / Pixel format                                   
    FULLFRAM= '1608x1104'          / Full Frame                                     
    ROI     = '1600x1100 at 0,0'   / ROI                                            
    FRAMSIZE=              3520000 / Frame size (Bytes)                             
    FRAMRATE=    3.392067663337556 / Frame rate (Hz)                                
    EXPTIME =             0.099996 / Exposure time (seconds)                        
    GAINCONV= 'LCG     '           / Gain Conv.                                     
    GAMMAENA=                    F / Gamma Enable                                   
    GAMMAVAL=       0.800048828125 / Gamma Value                                    
    ACQUIMOD= 'SingleFrame'        / Acquisition mode                               
    FRMRATBD= '(min=1.0, max=3.3953648380635064)' / Framerate bounds                
    EXPTIMBD= '(min=14.0, max=30000003.0)' / Exp. time bounds                       
    GAINBD  = '(min=0.0, max=47.994294033026364)' / Gain bounds                     
    VOLTAGE =         9.7451171875 / Power Supply Voltage (V)                       
    CURRENT =       0.264404296875 / Power Supply Current (A)                       
    POWER   =    2.065127372741699 / Total Dissiapted Power (W)                     
    CAMTEMP =               38.625 / Camera Temperature (C)                         
    TEST1   =                 9999 / Extra header test 1                            
    TEST2   =                  999 / Extra header test 2                            
    TESTHDR3=                   -1 / Extra header test 3                            
    TESTHDR4=                   -2 / Extra header test 4                            
    CHECKSUM= 'ReALSZ4LRb9LRZ9L'   / HDU checksum updated 2021-12-12T13:57:15       
    DATASUM = '1576855900'         / data unit checksum updated 2021-12-12T13:57:15 
    END                                                                             




Compression
-----------
The ``-c`` or ``--compress`` option is to choose one of the `compression algorithms <https://docs.astropy.org/en/latest/io/fits/api/images.html#astropy.io.fits.CompImageHDU>`_.

You can choose one of ['NO', 'R1', 'RO', 'P1', 'G1', 'G2', 'H1'] that respectively represents ['None', 'RICE_1', 'RICE_ONE', 'PLIO_1', 'GZIP_1', 'GZIP_2', 'HCOMPRESS_1'].

.. code-block:: console

    $ lvmcam start --debug
    [DEBUG]: [0.997 s]: async _expose_internal
    [DEBUG]: [1.101 s]: async expose_real_cam
    [DEBUG]: [0.995 s]: async _expose_internal
    [DEBUG]: [1.183 s]: async expose_real_cam
    [DEBUG]: [0.996 s]: async _expose_internal
    [DEBUG]: [1.170 s]: async expose_real_cam
    [DEBUG]: [0.996 s]: async _expose_internal
    [DEBUG]: [1.092 s]: async expose_real_cam
    [DEBUG]: [0.996 s]: async _expose_internal
    [DEBUG]: [1.225 s]: async expose_real_cam
    [DEBUG]: [0.995 s]: async _expose_internal
    [DEBUG]: [1.217 s]: async expose_real_cam
    [DEBUG]: [0.995 s]: async _expose_internal
    [DEBUG]: [1.178 s]: async expose_real_cam


.. code-block:: console

    $ clu
    lvmcam connect
    05:28:26.621 lvmcam > 
    05:28:30.889 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    lvmcam expose -v -c NO 0.5 1 sci.agw
    05:28:59.416 lvmcam > 
    05:29:00.515 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211212/lvm.sci.agw-00000001.fits"
        }
    }
    lvmcam expose -v -c R1 0.5 1 sci.agw
    05:29:06.219 lvmcam > 
    05:29:07.404 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211212/lvm.sci.agw-00000002.fits"
        }
    }
    lvmcam expose -v -c RO 0.5 1 sci.agw
    05:29:11.742 lvmcam > 
    05:29:12.912 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211212/lvm.sci.agw-00000003.fits"
        }
    }
    lvmcam expose -v -c P1 0.5 1 sci.agw
    05:29:17.297 lvmcam > 
    05:29:18.389 lvmcam : {
        "PATH": {
            "0": "data out of range for PLIO compression (0 - 2**24)"
        }
    }
    lvmcam expose -v -c G1 0.5 1 sci.agw
    05:29:24.555 lvmcam > 
    05:29:25.778 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211212/lvm.sci.agw-00000004.fits"
        }
    }
    lvmcam expose -v -c G2 0.5 1 sci.agw
    05:29:29.583 lvmcam > 
    05:29:30.801 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211212/lvm.sci.agw-00000005.fits"
        }
    }
    lvmcam expose -v -c H1 0.5 1 sci.agw
    05:29:35.534 lvmcam > 
    05:29:36.712 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211212/lvm.sci.agw-00000006.fits"
        }
    }

.. code-block:: console

    $ ls -alh
    total 14M
    drwxrwxr-x 2 mgjeon mgjeon 4.0K Dec 12 14:29 .
    drwxrwxr-x 5 mgjeon mgjeon 4.0K Dec 12 14:26 ..
    -rw-rw-r-- 1 mgjeon mgjeon 3.4M Dec 12 14:29 lvm.sci.agw-00000001.fits
    -rw-rw-r-- 1 mgjeon mgjeon 2.3M Dec 12 14:29 lvm.sci.agw-00000002.fits
    -rw-rw-r-- 1 mgjeon mgjeon 2.3M Dec 12 14:29 lvm.sci.agw-00000003.fits
    -rw-rw-r-- 1 mgjeon mgjeon 1.9M Dec 12 14:29 lvm.sci.agw-00000004.fits
    -rw-rw-r-- 1 mgjeon mgjeon 1.8M Dec 12 14:29 lvm.sci.agw-00000005.fits
    -rw-rw-r-- 1 mgjeon mgjeon 1.7M Dec 12 14:29 lvm.sci.agw-00000006.fits