#!/bin/bash

# Build and run in one command
xhost +local:docker
echo "Quick build and run:"
docker build --no-cache -t mtllm-oopsla2025 .

docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  mtllm-oopsla2025

# Test the installation inside container
echo ""