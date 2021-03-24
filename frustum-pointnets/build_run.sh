#!/bin/bash
# Build docker image
docker build \
--file=tensorflow.Dockerfile \
--tag="frustum-pointnet:0.1" \
.
# Create folder that will be binded to container (where repo is available)
mkdir -p src
# Create container with gpu capabilities
docker create \
--gpus all \
--interactive \
--tty \
--rm \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-e DISPLAY=unix$DISPLAY \
--name=frustum-pointnet \
--publish-all \
--mount type=bind,source="$(pwd)/src",target=/home/pepper/GitHub \
--workdir /home/pepper/GitHub \
frustum-pointnet:0.1

docker start frustum-pointnet

# Clone custom Mask-RCNN repo as the user of the host system
cd $(pwd)/src
git clone https://github.com/lemontyc/frustum-pointnets.git

# Print ports
docker port frustum-pointnet