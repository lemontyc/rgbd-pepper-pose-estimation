#!/bin/bash

get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

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
