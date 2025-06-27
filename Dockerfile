FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    nano \
    python3-pygame \
    libx11-6 \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Clone the repository
RUN git clone --recurse-submodules https://github.com/Jayanaka-98/mtllm-oopsla2025.git . \
    && ls -la

# Install MTLLM with dependencies for evaluation
RUN pip install --upgrade pip && \
    pip install "mtllm[openai, ollama, tools]==0.3.8"

# Install evaluation requirements separately
RUN if [ -f "eval/requirements.txt" ]; then \
        echo "Found eval/requirements.txt, installing..." && \
        pip install -r "eval/requirements.txt"; \
    else \
        echo "eval/requirements.txt not found, listing directory contents:" && \
        find . -name "requirements.txt" -type f; \
    fi

# Install Ollama for local model support (optional)
RUN curl -fsSL https://ollama.ai/install.sh | sh || echo "Ollama installation completed"

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "=== MTLLM OOPSLA 2025 Artifact ===" \n\
echo "Repository: https://github.com/Jayanaka-98/mtllm-oopsla2025" \n\
exec "$@"' > /usr/local/bin/entrypoint.sh \
    && chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command
CMD ["bash"]