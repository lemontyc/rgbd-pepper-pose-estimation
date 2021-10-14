#!/bin/bash

get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

# Check if Mas R-CNN repo has been downloaded
# https://github.com/lemontyc/Mask_RCNN
if [ -d "../workspace/Mask_RCNN" ] 
then
    echo "Skipping Mask R-CNN download"
else
     echo "Mask R-CNN not found, downloading"
    cd ../
    git submodule update --init --recursive
fi

# Build docker image
docker build \
--file=../docker/tensorflow.Dockerfile \
--tag="m_rcnn:1.0" \
../workspace

# Get absolut path to workspace folder
myabsfile=$(get_abs_filename "../workspace")

# Create container with gpu capabilities
docker create \
--gpus all \
--interactive \
--tty \
--rm \
--name=m_rcnn \
--mount type=bind,source="$myabsfile",target=/workspace \
m_rcnn:1.0

docker start m_rcnn