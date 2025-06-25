#!/bin/bash

# Build the Docker image
echo "Building MTLLM Docker image..."
docker build -t mtllm-oopsla2025 .

# Option 3: Run with docker-compose (recommended)
echo "To run with docker-compose (recommended):"
echo "export OPENAI_API_KEY=\"your-key\""
echo "export ANTHROPIC_API_KEY=\"your-key\""
echo "docker-compose up"
echo ""

# Build and run in one command
echo "Quick build and run:"
docker build -t mtllm-oopsla2025 . && docker run -it --rm mtllm-oopsla2025

# Test the installation inside container
echo ""