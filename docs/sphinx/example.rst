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
            "0": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000001.fits",
            "1": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000002.fits",
            "2": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000003.fits"
        }
    }
    lvmcam expose -v -r 00h42m44s -d 41d16m09s -K 10 -f 1800 1 3 sci.agw
    00:35:22.831 lvmcam > 
    00:35:27.655 lvmcam : {
        "PATH": {
            "0": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000004.fits",
            "1": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000005.fits",
            "2": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/lvm/sci/agw/20211203/lvm.sci.agw-00000006.fits"
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
            "0": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000001.fits",
            "1": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000002.fits",
            "2": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000003.fits"
        }
    }
    lvmcam expose 1 3 test
    00:25:54.139 lvmcam > 
    00:25:57.165 lvmcam : {
        "PATH": {
            "0": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000004.fits",
            "1": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000005.fits",
            "2": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/test/20211203/lvm.test-00000006.fits"
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
            "0": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/testshot.fits"
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
            "0": "/home/sumin/dev_lvmcam/lvmcam/python/lvmcam/assets/testshot.fits"
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
 

Compression
-----------

