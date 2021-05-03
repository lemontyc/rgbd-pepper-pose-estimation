#!/bin/bash

# Clone repo into a temporal folder. The google TF2 Dockerfile copies the repo from the temporal folder to the image
# The tmeporal folder will be deleted to free space in the host device later
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
cd ../..

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