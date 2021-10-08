#!/bin/bash
# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Script to download and preprocess the COCO data set for detection.
#
# The outputs of this script are TFRecord files containing serialized
# tf.Example protocol buffers. See create_coco_tf_record.py for details of how
# the tf.Example protocol buffers are constructed and see
# http://cocodataset.org/#overview for an overview of the dataset.
#
# usage:
#  bash preprocess_pepper.sh /data-dir/pepper
set -e
set -x


if [ -z "$1" ]; then
  echo "usage preprocess_pepper.sh [data dir]"
  exit
fi

#sudo apt install -y protobuf-compiler python-pil python-lxml\
#  python-pip python-dev git unzip

#pip install Cython git+https://github.com/cocodataset/cocoapi#subdirectory=PythonAPI

echo "Cloning Tensorflow models directory (for conversion utilities)"
if [ ! -e tf-models ]; then
  git clone http://github.com/tensorflow/models tf-models
fi

(cd tf-models/research && protoc object_detection/protos/*.proto --python_out=.)

UNZIP="unzip -nq"

# Create the output directories.
OUTPUT_DIR="${1%/}"
SCRATCH_DIR="${OUTPUT_DIR}/raw-data"
mkdir -p "${OUTPUT_DIR}"
mkdir -p "${SCRATCH_DIR}"
CURRENT_DIR=$(pwd)

cd ${SCRATCH_DIR}

# Image paths.
BASE_IMAGE_URL="http://images.cocodataset.org/zips"

TRAIN_IMAGE_DIR="${SCRATCH_DIR}/train2021"

VAL_IMAGE_DIR="${SCRATCH_DIR}/val2021"

TEST_IMAGE_DIR="${SCRATCH_DIR}/test2021"

# Annotations Paths
TRAIN_OBJ_ANNOTATIONS_FILE="${SCRATCH_DIR}/annotations/instances_train2021.json"
VAL_OBJ_ANNOTATIONS_FILE="${SCRATCH_DIR}/annotations/instances_val2021.json"

# TRAIN_CAPTION_ANNOTATIONS_FILE="${SCRATCH_DIR}/annotations/captions_train2017.json"
# VAL_CAPTION_ANNOTATIONS_FILE="${SCRATCH_DIR}/annotations/captions_val2017.json"

# Test Info
# TESTDEV_ANNOTATIONS_FILE="${SCRATCH_DIR}/annotations/image_info_test-dev2017.json"
TESTDEV_ANNOTATIONS_FILE="${SCRATCH_DIR}/annotations/instances_val2021.json"

# # Build TFRecords of the image data.
cd "${CURRENT_DIR}"

# Setup packages
touch tf-models/__init__.py
touch tf-models/research/__init__.py

# Run our conversion
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

PYTHONPATH="tf-models:tf-models/research" python $SCRIPT_DIR/create_coco_tf_record.py \
  --logtostderr \
  --include_masks \
  --train_image_dir="${TRAIN_IMAGE_DIR}" \
  --val_image_dir="${VAL_IMAGE_DIR}" \
  --test_image_dir="${TEST_IMAGE_DIR}" \
  --train_object_annotations_file="${TRAIN_OBJ_ANNOTATIONS_FILE}" \
  --val_object_annotations_file="${VAL_OBJ_ANNOTATIONS_FILE}" \
  --testdev_annotations_file="${TESTDEV_ANNOTATIONS_FILE}" \
  --output_dir="${OUTPUT_DIR}"
  # --train_caption_annotations_file="${TRAIN_CAPTION_ANNOTATIONS_FILE}" \
  # --val_caption_annotations_file="${VAL_CAPTION_ANNOTATIONS_FILE}" \

mv ${SCRATCH_DIR}/annotations/ ${OUTPUT_DIR}
