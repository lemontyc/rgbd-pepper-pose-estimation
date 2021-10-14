#!/bin/bash
# Create container with gpu capabilities
docker create \
--gpus all \
--interactive \
--tty \
--rm \
--name=m_rcnn \
--publish-all \
--mount type=bind,source="$(pwd)/src",target=/home/pepper/GitHub \
--workdir /home/pepper/GitHub \
m_rcnn:0.1

docker start m_rcnn

# And install it
docker exec  -w /home/pepper/GitHub/Mask_RCNN m_rcnn pip install -r requirements.txt
docker exec  -w /home/pepper/GitHub/Mask_RCNN m_rcnn python setup.py install

# Print ports
docker port m_rcnn