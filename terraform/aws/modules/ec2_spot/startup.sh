#!/bin/bash
set -x

echo "executing startup script"
sudo dnf -y install docker
sudo service docker start
sudo docker pull asia-northeast3-docker.pkg.dev/model-sphere-399315/spot/spot_test:latest
# sudo usermod -a -G docker ec2-user
sudo docker run -v /home/ec2-user/:/vol/ asia-northeast3-docker.pkg.dev/model-sphere-399315/spot/spot_test:latest
