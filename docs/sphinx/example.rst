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
    03:30:31.526 lvmcam > 
    03:30:36.461 lvmcam i {
        "CAMERA": {
            "name": "sci.agw",
            "uid": "19283193"
        }
    }
    03:30:36.467 lvmcam : 
    lvmcam expose -r "00h42m44s" -d "41d16m09s" -K 10 -f 1800 0.1 3 sci.agw
    03:30:41.867 lvmcam > 
    03:30:45.230 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459519/sci.agw-00000001.fits",
            "1": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459519/sci.agw-00000002.fits",
            "2": "/home/mgjeon/lvmcam/python/lvmcam/assets/2459519/sci.agw-00000003.fits"
        }
    }
    03:30:45.233 lvmcam : 
    lvmcam expose -p "foo/bar" -r 10.68 -d 41.27 -K 10 -f 1800 0.1 3 sci.agw
    
    03:32:36.491 lvmcam > 
    03:32:39.825 lvmcam i {
        "PATH": {
            "0": "/home/mgjeon/lvmcam/foo/bar/2459519/sci.agw-00000001.fits",
            "1": "/home/mgjeon/lvmcam/foo/bar/2459519/sci.agw-00000002.fits",
            "2": "/home/mgjeon/lvmcam/foo/bar/2459519/sci.agw-00000003.fits"
        }
    }
    03:32:39.828 lvmcam : 
 

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
    