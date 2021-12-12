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
    00:25:42.254 lvmcam > 
    00:25:42.295 lvmcam i {
        "CAMERA": {
            "name": "test",
            "uid": "-1"
        }
    }
    00:25:42.296 lvmcam : 
    lvmcam expose 0.1 3 test
    00:25:49.450 lvmcam > 
    00:25:49.772 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000001.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000002.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000003.fits"
        }
    }
    lvmcam expose 1 3 test
    00:25:54.139 lvmcam > 
    00:25:57.165 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000004.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000005.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000006.fits"
        }
    }
    

The 'test' camera is fake camera. All images captured by the 'test' camera are just files copied from `python/lvmcam/actor/example`.


Test shot
---------  

The ``--testshot`` or ``-t`` option in ``expose`` command makes one ``testshot.fits`` file that is always overwritten. 
The ``NUM`` argument of ``expose`` is ignored.

.. code-block:: console

    $ clu
    lvmcam connect -t
    00:26:48.589 lvmcam > 
    00:26:48.637 lvmcam i {
        "CAMERA": {
            "name": "test",
            "uid": "-1"
        }
    }
    00:26:48.642 lvmcam : 
    lvmcam expose -t 0.1 3 test
    00:26:57.522 lvmcam > 
    00:26:57.636 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/testshot.fits"
        }
    }
    lvmcam disconnect
    00:27:02.609 lvmcam > 
    00:27:02.610 lvmcam i {
        "text": "Cameras have been removed"
    }
    00:27:02.611 lvmcam : 
    lvmcam connect
    00:27:05.834 lvmcam > 
    00:27:10.100 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    00:27:10.107 lvmcam : 
    lvmcam expose -t -r 00h42m44s -d 41d16m09s -K 10 -f 1800 1 3 sci.agw
    00:27:35.791 lvmcam > 
    00:27:37.398 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/testshot.fits"
        }
    }
 


Show commands
--------------

The 'Available' means that the camera can be connected.

.. code-block:: console

    $ clu
    lvmcam show all
    00:28:19.037 lvmcam > 
    00:28:20.374 lvmcam i {
        "ALL": {
            "test": "Unavailable | uid: -1",
            "sci.agw": "Available | uid: 19283193",
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
    00:28:20.385 lvmcam : 
 

``lvmcam show connection`` shows all connected cameras. This reply is similar to that of ``lvmcam connect``.

.. code-block:: console

    $ clu
    lvmcam show connection
    00:28:45.824 lvmcam > 
    00:28:45.825 lvmcam e {
        "text": "There are no connected cameras"
    }
    lvmcam connect -t
    00:28:52.466 lvmcam > 
    00:28:52.514 lvmcam i {
        "CAMERA": {
            "name": "test",
            "uid": "-1"
        }
    }
    00:28:52.515 lvmcam : 
    lvmcam show connection
    00:28:56.137 lvmcam > 
    00:28:56.138 lvmcam i {
        "CONNECTED": {
            "name": "test",
            "uid": "-1"
        }
    }
    00:28:56.139 lvmcam : 
    lvmcam connect
    00:28:58.914 lvmcam > 
    00:28:58.962 lvmcam e {
        "text": "Cameras are already connected"
    }
    lvmcam disconnect
    00:29:01.823 lvmcam > 
    00:29:01.825 lvmcam i {
        "text": "Cameras have been removed"
    }
    00:29:01.826 lvmcam : 
    lvmcam connect
    00:29:06.434 lvmcam > 
    00:29:10.680 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    00:29:10.688 lvmcam : 
    lvmcam show connection
    00:29:13.998 lvmcam > 
    00:29:14.000 lvmcam i {
        "CONNECTED": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    00:29:14.002 lvmcam : 
 

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

The ``--header`` option is passed 'JSON header' like `archon <https://github.com/sdss/archon/blob/c28080d145072dc80dedff111d6d589a7fd195ff/archon/actor/commands/expose.py#L145>`_. The rule for 'JSON header' is ``{Header1: (Value1, Comment1), Header2: (Value2, Comment2) ...}``.


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
    05:28:30.896 lvmcam : 
    lvmcam expose 0.1 1 sci.agw
    05:28:32.941 lvmcam > 
    05:28:33.656 lvmcam : {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211212/lvm.sci.agw-00000001.fits"
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