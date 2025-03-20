#!/bin/bash

# Build the Docker image for Raspberry Pi (ARM architecture)
echo "Building Docker image for edge-cam..."
docker build -t edge-cam:latest .

# Run the container
echo "Starting edge-cam container..."
docker compose up -d

echo "Edge-cam is now running on http://localhost:8000"
echo "Check logs with: docker compose logs -f"