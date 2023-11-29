#!/bin/bash
set -x

PID=0 
set_flag="$1"

# set_flag="false"
# while [ $# -gt 0 ]; do
#     echo $1
#     echo $2
#     case $1 in 
#     --resume) set_flag="$2"
#     esac
#     shift
# done

flag=""
if [ "$set_flag" = "true" ]; then
    flag="--resume"
fi

# Define cleanup procedure
cleanup() {
    echo "Executing clean up script..."
    if [ $PID -ne 0 ]; then
        kill -SIGTERM "$PID"
        wait "$PID"
    fi
    exit 143;  # propogate SIGTERM
}

#Trap SIGTERM
trap 'kill ${!}; cleanup' SIGTERM

# replace with actual execution code 
python run.py $flag &
PID=${!}

# runs in the background forever
tail -f /dev/null &
wait ${!}
