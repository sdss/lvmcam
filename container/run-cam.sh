#!/usr/bin/bash

LVMT_PATH=/root/lvmcam
LVMT_CAM=${LVMT_CAM:="lvm.sci.agcam"}
LVMT_CAM_TYPE=${LVMT_CAM_TYPE:="araviscam"}
LVMT_DATA_ROOT="${LVM_DATA_ROOT:=${HOME}/data}"
LVMT_RMQ=${LVMT_RMQ:=localhost}


echo $LVMT_DEBUG
if [ $LVMT_DEBUG ]; then 
    export PYTHONPATH=$LVMT_PATH/python/
fi

sed "s/camtype: .*/camtype: $LVMT_CAM_TYPE/; s/host: .*$/host: $LVMT_RMQ/" < $LVMT_PATH/python/lvmcam/etc/$LVMT_CAM.yml \
            > $LVMT_PATH/python/lvmcam/etc/$LVMT_CAM_$LVMT_RMQ.yml

python3 $LVMT_PATH/python/lvmcam/__main__.py -c $LVMT_PATH/python/lvmcam/etc/$LVMT_CAM_$LVMT_RMQ.yml --verbose start --debug
