#!/bin/bash

# Clone repo into a temporal folder. The google TF2 Dockerfile copies the repo from the temporal folder to the image
# The tmeporal folder will be deleted to free space in the host device later
mkdir -p tmp
cd $(pwd)/tmp
git clone https://github.com/lemontyc/models.git

# Build docker image from the root of the git repository (inside the models directory)
cd models
docker build \
--file=research/object_detection/dockerfiles/tf2/Dockerfile \
--tag="od:2.4.0" \
.

# Delete temporal folder
cd ../..
rm -rf tmp/


# Run it
docker run -it od:2.4.0
