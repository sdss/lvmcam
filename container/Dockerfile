FROM ubuntu:20.04

LABEL email="mgjeon@khu.ac.kr"
LABEL name="Mingyu Jeon"

SHELL ["/bin/bash", "-c"]

RUN apt update -y && \
    apt install -y wget && \
    echo "8\n7\n" | apt install -y software-properties-common && \
    echo "30\n1\n" | apt install -y keyboard-configuration && \
    wget -qO - https://zeroc.com/download/GPG-KEY-zeroc-release-B6391CB2CFBA643D | apt-key add - && \
    apt-add-repository "deb http://zeroc.com/download/ice/3.7/ubuntu20.04 stable main" && \
    wget -qO - https://svn.mpia.de/repo/linux/ubuntu/archive.key | apt-key add - && \
    echo "deb https://svn.mpia.de/repo/linux/ubuntu focal main" > /etc/apt/sources.list.d/mpia.list

RUN apt update -y && \
    apt-get install -y git curl make build-essential libssl-dev zlib1g-dev && \
    apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev && \
    apt-get install -y libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl && \
    apt-get install -y libcairo2-dev libjpeg-dev libgif-dev debhelper cmake gtk-doc-tools && \
    apt-get install -y libusb-1.0-0-dev libaudit-dev libgirepository1.0-dev libglib2.0-dev && \
    apt-get install -y libnotify-dev libgtk-3-dev libgstreamer-plugins-base1.0-dev meson && \
    apt-get install -y python3-pip python3-dev intltool libxml2-dev
    
RUN mkdir -p /root/aravis && \
    cd /root/aravis && \
    wget http://ftp.br.debian.org/debian/pool/main/a/aravis/aravis_0.8.6.orig.tar.xz && \
    wget http://ftp.br.debian.org/debian/pool/main/a/aravis/aravis_0.8.6-1.dsc && \
    wget http://ftp.br.debian.org/debian/pool/main/a/aravis/aravis_0.8.6-1.debian.tar.xz && \
    tar xvJf aravis_0.8.6.orig.tar.xz && \
    cd aravis-0.8.6 && \
    tar xvJf ../aravis_0.8.6-1.debian.tar.xz && \
    dpkg-buildpackage -rfakeroot -b -uc -us && \
    cd .. && \
    dpkg -i *.deb && \
    apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y gir1.2-aravis-0.8 aravis-tools aravis-tools-cli && \
    rm -rf /root/aravis

########## virtualenv
# RUN cd /root && \
#     git clone https://github.com/sdss/lvmcam.git && \
#     cd lvmcam && \
#     sed -i '/    araviscam/c\    araviscam: False' python/lvmcam/etc/camtype.yaml && \
#     sed -i '/    skymakercam/c\    skymakercam: True' python/lvmcam/etc/camtype.yaml

# RUN cd /root/lvmcam && \
#     pip install virtualenv && \
#     virtualenv venv --python=python3.8 && \
#     source venv/bin/activate && \
#     pip install poetry && \
#     poetry install

# ENV VIRTUAL_ENV=${HOME}/lvmcam/venv
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
########## virtualenv

########## pyenv
RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
RUN apt -y install make build-essential libssl-dev zlib1g-dev libbz2-dev \
                           libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
                           xz-utils tk-dev libffi-dev

RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

RUN source ~/.bashrc

ENV PATH=/root/.pyenv/bin:$PATH

RUN cd /root && \
    git clone https://github.com/sdss/lvmcam.git && \
    cd lvmcam

RUN cd /root/lvmcam && \
    pyenv install 3.9.8 && \
    pyenv virtualenv 3.9.8 lc && \
    pyenv local lc

RUN cd /root/lvmcam && \
    bash -i -c "\
    source ~/.bashrc && \
    pyenv activate lc && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry install"
    
# RUN pyenv rehash
ENV PATH=/root/.pyenv/shims:$PATH
ENV PATH=/root/.pyenv/versions/lc/bin/:$PATH
########## pyenv

WORKDIR /root/lvmcam

COPY ./container/run-cam.sh /root/lvmcam/container

RUN chmod +x ./container/run-cam.sh

CMD ["/root/lvmcam/container/run-cam.sh"]