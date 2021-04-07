#!/bin/bash

# Create folder that will bind to container
mkdir -p src

# Create container with gpu capabilities
docker create \
--gpus all \
--interactive \
--tty \
--rm \
--name=f-convnet \
--publish-all \
--mount type=bind,source="$(pwd)/src",target=/home/pepper/GitHub \
--workdir /home/pepper/GitHub \
f-convnet:0.1

docker start f-convnet

# And install it
docker exec  -w /home/pepper/GitHub/frustum-convnet f-convnet pip install -r requirements.txt
# docker exec  -w /home/pepper/GitHub/Mask_RCNN f-convnet python setup.py install

# Print ports
docker port f-convnet