# Stage 1: Build the Frontend
FROM node:16 as frontend

# Set working directory inside the container for frontend
WORKDIR /app/mumbai-housing-project

# Copy the frontend folder to the container
COPY mumbai-housing-project/ .

# Install dependencies for React app
RUN npm install

# Build the React app
RUN npm run build

# Stage 2: Set up QGIS, GDAL, and Flask backend
FROM ubuntu:20.04

# Set environment variables to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV QT_QPA_PLATFORM=offscreen
ENV DISPLAY=:99
ENV XDG_RUNTIME_DIR=/tmp/runtime-dir
ENV LD_LIBRARY_PATH=/usr/lib:/usr/lib/x86_64-linux-gnu

# Set QGIS environment variables
ENV PYTHONPATH=/usr/share/qgis/python:/usr/share/qgis/python/plugins
ENV LD_LIBRARY_PATH=/usr/lib
ENV QGIS_PREFIX_PATH=/usr
ENV QT_QPA_FONTDIR=/usr/share/fonts/truetype/

# Install prerequisites and configure apt
RUN apt-get update && apt-get install -y \
    software-properties-common \
    lsb-release \
    gnupg \
    curl \
    wget \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Create directory for keyrings and add QGIS repository
RUN mkdir -p /etc/apt/keyrings && \
    wget -qO /etc/apt/keyrings/qgis-archive-keyring.gpg https://download.qgis.org/downloads/qgis-archive-keyring.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/qgis-archive-keyring.gpg] https://qgis.org/ubuntu-ltr focal main" | tee /etc/apt/sources.list.d/qgis.list

# Update package lists
RUN apt-get update

# Install QGIS, GDAL, and related packages
RUN apt-get install -y \
    python3-pip \
    python3-dev \
    qgis \
    qgis-plugin-grass \
    python3-qgis \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_VERSION=3.1
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Create runtime directory for XDG and fix permissions
RUN mkdir -p /tmp/runtime-dir && chmod 700 /tmp/runtime-dir

# Set working directory inside the container for backend
WORKDIR /app/backend

# Copy the backend folder to the container
COPY backend/ .

# Copy the requirements.txt from the root of the project
COPY requirements.txt .

# Install Python dependencies for Flask app
RUN pip3 install -r requirements.txt

# Copy the React build files from Stage 1 to the backend's 'frontend-build' folder
COPY --from=frontend /app/mumbai-housing-project/build ./frontend-build

# Create QGIS initialization script
RUN echo '#!/usr/bin/python3\n\
import os\n\
import sys\n\
from qgis.core import *\n\
from qgis.analysis import QgsNativeAlgorithms\n\
\n\
# Initialize QGIS Application\n\
QgsApplication.setPrefixPath("/usr", True)\n\
qgs = QgsApplication([], False)\n\
qgs.initQgis()\n\
\n\
# Initialize Processing\n\
import processing\n\
from processing.core.Processing import Processing\n\
Processing.initialize()\n\
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())\n\
\n\
# Print success message\n\
print("QGIS environment initialized successfully!")\n' > /app/backend/initialize_qgis.py

# Create a script to start Xvfb and the application
RUN echo '#!/bin/bash\n\
mkdir -p /tmp/runtime-dir\n\
chmod 700 /tmp/runtime-dir\n\
Xvfb :99 -screen 0 1024x768x16 &\n\
sleep 1\n\
python3 initialize_qgis.py\n\
python3 server.py\n' > /start.sh && \
    chmod +x /start.sh

# Expose port for Flask and React
EXPOSE 8080

# Command to run the start script
CMD ["/start.sh"]