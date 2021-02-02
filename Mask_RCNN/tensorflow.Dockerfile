# Custom docker file based on Tensorflow 1.3.0.
# Used to train and run Mask-RCNN
#  :org:        ITESM QRO
#  :author:     Luis Montoya
#  :mail:       luis.montoya@exatec.tec.mx

# Custom image for tensorflow 1.3.0
FROM tensorflow/tensorflow:1.3.0-gpu-py3
# Install useful tools
RUN apt-get update -y
RUN apt-get install -y nano
RUN apt-get install -y git
RUN apt-get install -y libgl1-mesa-glx
RUN pip install --upgrade pip
# Create directory where we will clone the Mask-RCNN repo and clone repo
RUN mkdir -p /home/pepper/GitHub

# Set as workdir
WORKDIR /home/pepper/GitHub

EXPOSE 8888
EXPOSE 6006
