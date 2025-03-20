#!/bin/bash

# Generate requirements.txt if using poetry
if [ -f "pyproject.toml" ] && [ ! -f "requirements.txt" ]; then
    echo "Generating requirements.txt from poetry..."
    if command -v poetry &> /dev/null; then
        poetry export -f requirements.txt --output requirements.txt --without-hashes
    else
        echo "Poetry not found, creating basic requirements.txt..."
        cat > requirements.txt << EOF
fastapi>=0.95.0
uvicorn>=0.21.1
pydantic>=1.10.7
python-multipart>=0.0.6
EOF
    fi
fi

# Build and run with Docker Compose
docker compose up -d

# To run without docker-compose
# docker build -t edge-cam:latest .
# docker run -d --name edge-cam \
#   --privileged \
#   --network host \
#   -v $(pwd)/data:/app/data \
#   -v /dev:/dev \
#   -v /sys:/sys \
#   -v /var/run:/var/run \
#   -e PYTHONPATH=/usr/lib/python3/dist-packages:/usr/local/lib/python3/site-packages \
#   -e LOG_LEVEL=info \
#   -e UDEV=1 \
#   edge-cam:latest

echo "Edge-cam is now running on http://localhost:8000"
echo "Check logs with: docker compose logs -f"