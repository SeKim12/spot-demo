#!/bin/bash
:'
Startup script for GCE instances.
Install docker, pull training image, and run training with mounted volume. 
'
set -x

echo "Executing startup script..."
sudo snap install docker
sudo snap start docker
sleep 3
sudo docker pull asia-northeast3-docker.pkg.dev/model-sphere-399315/spot/spot_test:latest
sudo docker run -dv /home/seungwoo_simon_kim:/vol/ asia-northeast3-docker.pkg.dev/model-sphere-399315/spot/spot_test:latest
