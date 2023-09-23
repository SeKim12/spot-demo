#!/bin/bash

GSUTIL_OPTS="-m -o GSUtil:parallel_composite_upload_threshold=32M"
BUCKET_NAME="mdl-ckpts"
CHECKPOINT="vol/checkpoint.tar"
CONTAINER_ID="$(docker ps --format '{{.ID}}')"
IMAGE_TAG="$(docker ps --format '{{.Image}}')"

echo "Spot VM Shutting down, executing script..."

echo "Sending SIGTERM to container $CONTAINER_ID running $IMAGE_TAG"

TIMEFORMAT="Killed container $CONTAINER_ID in %R seconds"
time {
    docker kill $CONTAINER_ID
}

# upload interim data
gsutil "$GSUTIL_OPTS cp ${CHECKPOINT} ${GCS_PATH}/"
# su "${MY_USER}" -c "gsutil $GSUTIL_OPTS cp $CHECKPOINT gs://${BUCKET_NAME}/"

# shutdown
echo "Done uploading to ${GCS_PATH}/, shutting down."