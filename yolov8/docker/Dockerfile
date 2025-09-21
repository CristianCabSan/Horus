# Ultralytics YOLO 🚀, AGPL-3.0 license
# Builds ultralytics/ultralytics:latest image on DockerHub https://hub.docker.com/r/ultralytics/ultralytics
# Image is CUDA-optimized for YOLOv8 single/multi-GPU training and inference

# Start FROM PyTorch image https://hub.docker.com/r/pytorch/pytorch or nvcr.io/nvidia/pytorch:23.03-py3
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
RUN pip install --no-cache nvidia-tensorrt --index-url https://pypi.ngc.nvidia.com

# Downloads to user config dir
ADD https://ultralytics.com/assets/Arial.ttf https://ultralytics.com/assets/Arial.Unicode.ttf /root/.config/Ultralytics/

# Install linux packages
# g++ required to build 'tflite_support' package
RUN apt update \
    && apt install --no-install-recommends -y gcc git zip curl htop libgl1-mesa-glx libglib2.0-0 libpython3-dev gnupg g++
# RUN alias python=python3

RUN apt-get update && apt-get install -y libxcb-xinerama0 qt5-default

# Security updates
# https://security.snyk.io/vuln/SNYK-UBUNTU1804-OPENSSL-3314796
RUN apt upgrade --no-install-recommends -y openssl tar

# Create working directory
RUN mkdir -p /usr/src/ultralytics
WORKDIR /usr/src/ultralytics

# Copy contents
ADD . /usr/src/ultralytics
RUN rm -r /usr/src/ultralytics/tests
RUN rm -r /usr/src/ultralytics/docker
ADD ./.github /usr/src/ultralytics/.github

# Install pip packages
RUN python3 -m pip install --upgrade pip wheel
RUN pip install --no-cache -e . albumentations comet thop pycocotools onnx onnx-simplifier onnxruntime-gpu
RUN pip install --no-cache --pre -e . timm

# Set environment variables
ENV OMP_NUM_THREADS=1


# Usage -------------------------------------------------------------------------------------------------------

# For using webcam, first run:
# xhost +

# Build and run (Ubuntu)
# t=victory/victory:latest && sudo docker build -f docker/Dockerfile -t $t . && sudo docker run -it --ipc=host --device=/dev/video0:/dev/video0 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --gpus all $t

# Build and run (Windows)
# t=victory/victory:latest && sudo docker build -f docker/Dockerfile -t $t . && sudo docker run -it --ipc=host --gpus all $t

# Run detector on webcam (once inside container)
# yolo detect predict model=weights/yolo.pt source=0 show
 
# Kill all
# sudo docker kill $(sudo docker ps -q)

# Kill all image-based
# sudo docker kill $(sudo docker ps -qa --filter ancestor=victory/victory:latest)

# Clean up
# sudo docker system prune -a --volumes