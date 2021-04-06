# Custom docker file based on PyTorch 1.0.
# Used to train and run Mask-RCNN
#  :org:        ITESM QRO
#  :author:     Luis Montoya
#  :mail:       luis.montoya@exatec.tec.mx

# Custom image for tensorflow 1.0
FROM nvcr.io/nvidia/pytorch:19.01-py3

# Install useful tools
RUN apt-get update -y
RUN apt-get install -y libboost-dev
# Create directory where we will clone the Mask-RCNN repo and clone repo
RUN mkdir -p /home/pepper/GitHub

# Set as workdir
WORKDIR /home/pepper/GitHub

# EXPOSE 8888
# EXPOSE 6006
