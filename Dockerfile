FROM debian:bullseye

# Install needed packages first
RUN apt-get update && apt-get install -y \
    gnupg \
    wget \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Add Raspberry Pi OS repositories with proper key
RUN wget -O - https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | apt-key add - && \
    echo "deb http://archive.raspberrypi.org/debian/ bullseye main" > /etc/apt/sources.list.d/raspi.list

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcamera0 \
    python3-libcamera \
    python3-picamera2 \
    python3-pyqt5 \
    v4l-utils \
    libcamera-apps \
    || apt-get install -y python3-picamera2 v4l-utils

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt* ./

# Install Python dependencies
RUN pip3 install -r requirements.txt || echo "No requirements.txt found, continuing anyway"

# Copy application code
COPY . .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]