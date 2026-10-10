FROM mcr.microsoft.com/devcontainers/python:3.11

# Install any additional system dependencies if needed
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    && apt-get clean -y

# Set working directory
WORKDIR /workspace

# Set environment variables
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Default command
CMD ["sleep", "infinity"]
