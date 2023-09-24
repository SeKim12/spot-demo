#!/bin/bash
:'
Shutdown script for GCE instances.
Stops the running docker container (if not killed already) and uploads to GCS. 
SIGTERM is gracefully handled by container entrypoint script.
'
set -x 

CKPT_PATH="/home/seungwoo_simon_kim/checkpoint.tar"
GCS_PATH="gs://mdl-ckpts/"

CONTAINER_ID="$(docker ps --format '{{.ID}}')"

echo "Detected Spot VM preemption, executing shutdown script..."
[ -z "$CONTAINER_ID" ] && echo "no running containers" || sudo docker stop $CONTAINER_ID

su seungwoo_simon_kim -c "gsutil -m cp ${CKPT_PATH} ${GCS_PATH}"
echo "Finished uploading checkpoint to ${GCS_PATH}, exit shutdown script"