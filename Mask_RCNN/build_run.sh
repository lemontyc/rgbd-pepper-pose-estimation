#!/bin/bash

# Ceate a folder where the repo will be cloned. It will be used as a volume to share files
# between host and container
mkdir -p volume
cd $(pwd)/volume
git clone https://github.com/lemontyc/models.git

# Build docker image from the root of the git repository (inside the models directory)
cd models
docker build \
--file=research/object_detection/dockerfiles/tf2/Dockerfile \
--tag="od:2.4.0" \
.

# Move outside volume/
cd ../../

# Create container with gpu capabilities
docker create \
--gpus all \
--interactive \
--tty \
--rm \
--name=m_rcnn \
--mount type=bind,source="$(pwd)/volume/models",target=/home/tensorflow/models \
od:2.4.0

docker start m_rcnn