
lvmcam's documentation
======================
This is the documentation for the SDSS Python product lvmcam. The current version is |lvmcam_version|.

.. image:: https://img.shields.io/badge/python->3.8-blue
    :target: https://gitlab.com/group-name/project-name/commits/master
    :alt: Versions

.. image:: https://github.com/sdss/lvmcam/actions/workflows/test.yml/badge.svg
    :target: https://github.com/sdss/lvmcam/actions/workflows/test.yml
    :alt: Test

.. image:: https://readthedocs.org/projects/sdss-lvmcam/badge/?version=latest
    :target: https://sdss-lvmcam.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/sdss/lvmcam/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/sdss/lvmcam
    :alt: codecov

Quick Start
-----------

Clone the repository.

.. code-block:: console

  $ git clone https://github.com/sdss/lvmcam
  $ cd lvmcam 

Run install script. 

.. code-block:: console

  $ $SHELL install.sh

Set the python 3.8+ virtual environment.

.. code-block:: console 

  $ pyenv install 3.8.12
  $ pyenv virtualenv 3.8.12 lvmcam-with-3.8.12
  $ pyenv local lvmcam-with-3.8.12

Install poetry and dependencies.

.. code-block:: console

  $ pip install --upgrade pip
  $ pip install poetry
  $ poetry install

Start lvmcam actor.

.. code-block:: console

  $ poetry run container_start --kill --name=lvm.cam

In another terminal, type ``clu`` and ``lvm.cam ping`` for test.

.. code-block:: console

  $ clu
  lvm.cam ping
      07:41:22.636 lvm.cam > 
      07:41:22.645 lvm.cam : {
          "text": "Pong."
          }

If errors occur when running ``$ poetry run ...``, run a command below to check whether there are some lvmcam containers.

.. code-block:: console

  $ podman ps -a

If there are some containers, run a command below to delete a specific container.

.. code-block:: console

  $ podman rm -f <CONTAINER ID>

If the error similar to below occurs, check whether ``python/lvmcam/etc/<ActorName>.yml`` is empty.

.. code-block:: console

  TypeError: __init__() missing 1 required positional argument: 'name'

  All children are gone. Parent is exiting...


.. toctree::
  :caption: Reference
  :maxdepth: 3
  :hidden:

  api
  actor-commands

.. toctree::
  :caption: Development
  :maxdepth: 3
  :hidden:

  example
  structure
  Changelog <changelog>
  GitHub Repository <https://github.com/sdss/lvmcam>
  Issues  <https://github.com/sdss/lvmcam/issues>
