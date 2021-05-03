#!/bin/bash

# Clone repo into src/
mkdir -p src
cd $(pwd)/src
git clone https://github.com/lemontyc/models.git

# Build docker image from the root of the git repository (inside the models directory)
docker build -f models/research/object_detection/dockerfiles/tf2/Dockerfile -t od .
# Run it
docker run -it od
