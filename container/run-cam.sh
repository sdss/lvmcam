#!/usr/bin/bash

LVMT_PATH=/root/lvmcam
LVMT_CAM=${LVMT_CAM:=sci}
LVMT_CAM_TYPE=${LVMT_CAM_TYPE:="skymakercam"}
LVMT_DATA_ROOT="${LVM_DATA_ROOT:=${LVMT_PATH}/data}"
LVMT_RMQ=${LVMT_RMQ:=localhost}

#while IFS="" read -r p || [ -n "$p" ]; do eval echo "\"$p\""; done < actor.yml > $LVMT_PATH/python/lvmcam/etc/$CAM_NAME.yml

sed "s/camtype: .*/camtype: $LVMT_CAM_TYPE/; s/host: .*$/host: $LVMT_RMQ/" < $LVMT_PATH/python/lvmcam/etc/lvm.$LVMT_CAM.agcam.yml \
            > $LVMT_PATH/python/lvmcam/etc/lvm.$LVMT_CAM.agcam_$LVMT_RMQ.yml

lvmcam -c $LVMT_PATH/python/lvmcam/etc/lvm.$LVMT_CAM.agcam_$LVMT_RMQ.yml start --debug
