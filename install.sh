#!/bin/sh

# Install RabbitMQ.
sudo apt-get install -y erlang rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# Install the dependencies for pyenv, poetry, and Aravis.
sudo apt-get install -y git curl make build-essential libssl-dev zlib1g-dev
sudo apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev
sudo apt-get install -y libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
sudo apt-get install -y libcairo2-dev libjpeg-dev libgif-dev debhelper cmake gtk-doc-tools
sudo apt-get install -y libusb-1.0-0-dev libaudit-dev libgirepository1.0-dev libglib2.0-dev
sudo apt-get install -y libnotify-dev libgtk-3-dev libgstreamer-plugins-base1.0-dev meson
sudo apt-get install -y python3-pip python3-dev intltool libxml2-dev

# Install Aravis 0.8.
mkdir aravis
cd aravis
wget http://ftp.br.debian.org/debian/pool/main/a/aravis/aravis_0.8.6.orig.tar.xz
wget http://ftp.br.debian.org/debian/pool/main/a/aravis/aravis_0.8.6-1.dsc
wget http://ftp.br.debian.org/debian/pool/main/a/aravis/aravis_0.8.6-1.debian.tar.xz
tar xvJf aravis_0.8.6.orig.tar.xz
cd aravis-0.8.6
tar xvJf ../aravis_0.8.6-1.debian.tar.xz
dpkg-buildpackage -rfakeroot -b -uc -us
cd ..
sudo dpkg -i *.deb
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y gir1.2-aravis-0.8 aravis-tools aravis-tools-cli
cd ..
rm -rf aravis 

# Install podman
. /etc/os-release
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key" | sudo apt-key add -
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install podman

# Install lvmcam image.
podman pull ghcr.io/sdss/lvmcam:latest

# Install pyenv by using pyenv installer.
curl https://pyenv.run | bash

echo '
You should add the code below to ~/.bashrc or ~/.zshrc by using your preferred editor.

# pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"'