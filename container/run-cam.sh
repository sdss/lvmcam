#!/usr/bin/bash

LVMT_PATH=/root/lvmcam
# LVMT_CONFIG_PATH=$LVMT_PATH/config/planewave/$CAM_NAME

# setup_pwi4() {
#     mkdir -p $LVMT_CONFIG_PATH/Settings/
#     mkdir -p ~/PlaneWave\ Instruments/PWI4/
#     rm -rf ~/PlaneWave\ Instruments/PWI4/Settings
#     (cd ~/PlaneWave\ Instruments/PWI4/ && ln -s $LVMT_CONFIG_PATH/Settings/ )
#     if [ ! -f  $LVMT_CONFIG_PATH/Settings/PWI4.cfg ]; then
#         cp $LVMT_CONFIG_PATH/../pwi/Settings/PWI4.cfg $LVMT_CONFIG_PATH/Settings/PWI4.cfg
#     fi
#     if [ $PWI_SIMULATOR ]; then 
#         sed  -i "s/elmo/simulator/" $LVMT_CONFIG_PATH/Settings/PWI4.cfg
#     else
#         sed  -i "s/simulator/elmo/" $LVMT_CONFIG_PATH/Settings/PWI4.cfg
#     fi

#     mkdir -p $LVMT_CONFIG_PATH/Mount\ Tuning/
#     rm -rf ~/PlaneWave\ Instruments/Mount\ Tuning
#     (cd ~/PlaneWave\ Instruments/ && ln -s $LVMT_CONFIG_PATH/Mount\ Tuning/ )
#     mkdir -p $LVMT_PATH/data
#     (cd $PWI_PATH && ln -sf $LVMT_PATH/data data )
# }

# start_pwi4() {
#     cd $PWI_PATH
#     ./run-pwi4
# }

# max_pwi4() {
#     while [[ -z $(wmctrl -l) ]]; do sleep 0.1; done
#     wmctrl -r ':ACTIVE:' -b toggle,fullscreen
# }

# use_xrdp() {
#     echo -e "${PASSWD:-lvmt}\n${PASSWD:-lvmt}" | passwd
#     cp $LVMT_PATH/container/xrdp.ini /etc/xrdp/ 
#     Xvnc :2 -geometry 800x600 &
#     /usr/sbin/xrdp-sesman
#     /usr/sbin/xrdp
#     export DISPLAY=:2 
#     fluxbox &
# }

# use_vnc() {
#     echo -e "${PASSWD:-lvmt}\n${PASSWD:-lvmt}" | passwd
#     cp $LVMT_PATH/container/xrdp.ini /etc/xrdp/ 
#     Xvnc :0 -geometry $PWI_GEOM &
#     export DISPLAY=:0
#     fluxbox &
# }


start_actor() {
    # if [ ! -f $LVMT_PATH/python/lvmcam/etc/$CAM_NAME.yml ]; then
    #    cat $LVMT_PATH/python/lvmcam/etc/lvmcam.yml | sed "s/lvmcam/$CAM_NAME/; s/host: localhost/host: $LVMT_RMQ/" \
    #         > $LVMT_PATH/python/lvmcam/etc/$CAM_NAME.yml
    # #    sed  -i "s/elmo/simulator/" $LVMT_CONFIG_PATH/Settings/PWI4.cfg
    # fi

    cat $LVMT_PATH/python/lvmcam/etc/lvmcam.yml | sed "s/lvmcam/$CAM_NAME/; s/host: localhost/host: $LVMT_RMQ/" \
            > $LVMT_PATH/python/lvmcam/etc/$CAM_NAME.yml

    sleep 1

    if [ $CAM_VIRTUAL ]; then
        sed -i '/    araviscam/c\    araviscam: False' $LVMT_PATH/python/lvmcam/etc/camtype.yaml && \
        sed -i '/    skymakercam/c\    skymakercam: True' $LVMT_PATH/python/lvmcam/etc/camtype.yaml
    else
        sed -i '/    araviscam/c\    araviscam: True' $LVMT_PATH/python/lvmcam/etc/camtype.yaml && \
        sed -i '/    skymakercam/c\    skymakercam: False' $LVMT_PATH/python/lvmcam/etc/camtype.yaml
    fi
    
    # if [ $PWI_DEBUG ]; then 
    #     export PYTHONPATH=$LVMT_PATH/python
    # fi
    
    # python $LVMT_PATH/python/lvmcam/__main__.py -c $LVMT_PATH/python/lvmcam/etc/$CAM_NAME.yml start 

    if [ $CAM_DEBUG ]; then
        lvmcam -c $LVMT_PATH/python/lvmcam/etc/$CAM_NAME.yml start --debug
    else
        lvmcam -c $LVMT_PATH/python/lvmcam/etc/$CAM_NAME.yml start
    fi
    
}

# setup_pwi4

# if [ -z $DISPLAY ]; then
# #    use_xrdp
#     use_vnc
#     max_pwi4 &
# fi

start_actor

# start_pwi4
