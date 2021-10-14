# Custom docker file based on Tensorflow 1.3.0.
# Used to train and run Mask-RCNN
#  :org:        ITESM QRO
#  :author:     Luis Montoya
#  :mail:       luis.montoya@exatec.tec.mx

# Custom image for tensorflow 1.3.0
FROM tensorflow/tensorflow:1.3.0-gpu-py3

# RUN apt-get install apt-transport-https ca-certificates
RUN rm /etc/apt/sources.list.d/* && apt clean && apt update

# Install useful tools
RUN apt-get update -y
RUN apt-get install -y nano
RUN apt-get install -y git
RUN apt-get install -y libgl1-mesa-glx
RUN pip install --upgrade pip
# Create directory where we will clone the Mask-RCNN repo and clone repo
RUN mkdir -p /workspace

# Copy Mask Repo to container
COPY Mask_RCNN /workspace/Mask_RCNN

# Set as workdir
WORKDIR /workspace/Mask_RCNN

RUN pip install -r requirements.txt
RUN python setup.py install

# Set as workdir
WORKDIR /workspace