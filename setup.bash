#!/bin/bash

# Build and run in one command
echo "Quick build and run:"
docker build --no-cache -t mtllm-oopsla2025 . && docker run -it --rm mtllm-oopsla2025

# Test the installation inside container
echo ""