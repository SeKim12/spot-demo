#!/bin/bash
set -x

PID=0 

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
python run.py &
PID=${!}

# runs in the background forever
tail -f /dev/null &
wait ${!}
