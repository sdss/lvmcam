#!/bin/bash

PYTHON=/usr/local/bin/python3

# LVM_ACTOR # (Mandatory)

# LVM_RMQ_HOST #(Mandatory for kubernetes)
# LVM_ACTOR_ARGS # (Optional)
# LVM_DEBUG=true # (Optional)

LVM_ROOT=$HOME

umask 002

if [ ${LVM_DEBUG} ]; then
  LVM_ACTOR_PATH=$(ls -1 -d ${LVM_ROOT}/lvm/${LVM_ACTOR} ${LVM_ROOT}/${LVM_ACTOR} 2> /dev/null)/python/${LVM_ACTOR}
  export PYTHONPATH=$(ls -1 -d ${LVM_ROOT}/lvm/*/python ${LVM_ROOT}/lvm/basecam ${LVM_ROOT}/lvm/araviscam ${LVM_ROOT}/${LVM_ACTOR}/python 2>/dev/null | tr "\n" ":")
else
  LVM_ACTOR_PATH=$(${PYTHON} -c "import ${LVM_ACTOR} as _; print(_.__path__[0])")
fi
#echo ${LVM_ACTOR_PATH}
#echo $PYTHONPATH

export LVMT_DATA_ROOT="${LVM_DATA_ROOT:=/data}"

if [ $LVM_RMQ_HOST ]; then
  LVM_ACTOR_CONFIG_ABS=${LVM_ACTOR_PATH}/etc/${LVM_ACTOR_CONFIG:-${LVM_ACTOR}}_${LVM_RMQ_HOST}
  sed "s/host: .*$/host: $LVM_RMQ_HOST/" < ${LVM_ACTOR_PATH}/etc/${LVM_ACTOR_CONFIG}.yml \
            > ${LVM_ACTOR_CONFIG_ABS}.yml
  LVM_ACTOR_CONFIG_ARG="-c ${LVM_ACTOR_CONFIG_ABS}.yml"
elif  [ ${LVM_ACTOR_CONFIG} ]; then
  LVM_ACTOR_CONFIG_ARG="-c ${LVM_ACTOR_PATH}/etc/${LVM_ACTOR_CONFIG}.yml"
fi


echo "Using config: ${LVM_ACTOR_CONFIG_ARG}"

${PYTHON} ${LVM_ACTOR_PATH}/__main__.py ${LVM_ACTOR_CONFIG_ARG} ${LVM_ACTOR_ARGS} start --debug

#trap : TERM INT; ${PYTHON} ${LVM_ACTOR_PATH}/__main__.py ${LVM_ACTOR_CONFIG_ARG} ${LVM_ACTOR_ARGS} start --debug  & wait"]

if [ ${LVM_DEBUG} ]; then
   sleep INFINITY
fi
