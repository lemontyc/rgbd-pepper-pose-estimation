#!/bin/bash
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

# Print ports
docker port frustum-pointnet