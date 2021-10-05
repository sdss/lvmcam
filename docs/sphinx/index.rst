
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

.. image:: https://img.shields.io/travis/sdss/lvmcam
    :target: https://gitlab.com/group-name/project-name/commits/master
    :alt: Travis (.org)

.. image:: https://codecov.io/gh/sdss/lvmcam/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/sdss/lvmcam
    :alt: codecov

Quick Start
-----------

Prerequisite
^^^^^^^^^^^^
Install CLU.

.. code-block:: console

  $ pip install sdss-clu

Install RabbitMQ.

.. code-block:: console

  $ sudo apt-get install -y erlang rabbitmq-server
  $ sudo systemctl enable rabbitmq-server
  $ sudo systemctl start rabbitmq-server

Install pyenv by using pyenv installer.

.. code-block:: console

  $ curl https://pyenv.run | bash

You should add the code below to ``~/.bashrc`` by using your preferred editor.

.. code-block::

  # pyenv
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv init --path)"
  eval "$(pyenv virtualenv-init -)"

Install the dependencies for pyenv, poetry, and Aravis.

.. code-block:: console

  $ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev \
  libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl \
  libcairo2-dev libjpeg-dev libgif-dev debhelper cmake gtk-doc-tools \
  libusb-1.0-0-dev libaudit-dev libgirepository1.0-dev libglib2.0-dev \
  libnotify-dev libgtk-3-dev libgstreamer-plugins-base1.0-dev meson \
  python3-pip python3-dev intltool libxml2-dev

Install Aravis 0.8.

.. code-block:: console

  $ mkdir aravis
  $ cd aravis
  $ wget http://ftp.br.debian.org/debian/pool/main/a/aravis/aravis_0.8.6.orig.tar.xz
  $ wget http://ftp.br.debian.org/debian/pool/main/a/aravis/aravis_0.8.6-1.dsc
  $ wget http://ftp.br.debian.org/debian/pool/main/a/aravis/aravis_0.8.6-1.debian.tar.xz
  $ tar xvJf aravis_0.8.6.orig.tar.xz
  $ cd aravis-0.8.6
  $ tar xvJf ../aravis_0.8.6-1.debian.tar.xz
  $ dpkg-buildpackage -rfakeroot -b -uc -us
  $ cd ..
  $ sudo dpkg -i *.deb
  $ sudo apt-get update
  $ sudo apt-get upgrade
  $ sudo apt-get install -y gir1.2-aravis-0.8 aravis-tools aravis-tools-cli 


Install 
^^^^^^^

Clone the repository.

.. code-block:: console

  $ git clone https://github.com/sdss/lvmcam
  $ cd lvmcam 

Set the python 3.8+ virtual environment.

.. code-block:: console 

  $ pyenv install 3.9.7
  $ pyenv virtualenv 3.9.7 lvmcam-with-3.9.7
  $ pyenv local lvmcam-with-3.9.7

Install poetry and dependencies.

.. code-block:: console

  $ pip install poetry
  $ poetry install

Ping-pong test
^^^^^^^^^^^^^^^
Start lvmcam actor.

.. code-block:: console

  $ lvmcam start

In another terminal, type ``clu`` and ``lvmcam ping`` for test.

.. code-block:: console

  $ clu
  lvmcam ping
      07:41:22.636 lvmcam > 
      07:41:22.645 lvmcam : {
          "text": "Pong."
          }

Stop lvmcam actor.

.. code-block:: console

  $ lvmcam stop

Update
^^^^^^^

Pull the repository.

.. code-block:: console

  $ git pull

Update by using poetry.

.. code-block:: console

  $ poetry install



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
  Changelog <changelog>
  GitHub Repository <https://github.com/sdss/lvmcam>
  Issues  <https://github.com/sdss/lvmcam/issues>
