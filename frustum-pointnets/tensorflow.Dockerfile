# Custom docker file based on Tensorflow 1.4.0.
# Used to train and run Mask-RCNN
#  :org:        ITESM QRO
#  :author:     Luis Montoya
#  :mail:       luis.montoya@exatec.tec.mx

# Custom image for tensorflow 1.3.0
FROM tensorflow/tensorflow:1.4.1-gpu-py3
# Install/Update useful tools
RUN apt-get update -y
RUN apt-get install -y git
RUN pip3 install --upgrade pip
# Create directory where we will clone the Mask-RCNN repo and clone repo
RUN mkdir -p /home/pepper/GitHub
# Move into folder
WORKDIR /home/pepper/GitHub
# Clone repository
RUN git clone https://github.com/lemontyc/frustum-pointnets.git
WORKDIR /home/pepper/GitHub/frustum-pointnets/mayavi
RUN apt-get install -y python-vtk python-qt4 python-qt4-gl python-setuptools python-numpy python-configobj libgtk-3-dev
RUN pip3 install mayavi wxpython

WORKDIR /home/pepper/GitHub



EXPOSE 8888
EXPOSE 6006
