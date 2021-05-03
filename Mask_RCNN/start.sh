#!/bin/bash
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
