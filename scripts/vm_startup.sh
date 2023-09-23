#!/bin/bash

export GCS_PATH=$(curl "http://metadata.google.internal/computeMetadata/v1/instance/gcs_path" -H "Metadata-Flavor: Google")
echo "gcs path $GCS_PATH retrieved from metadata"