#!/usr/bin/env bash
# Render build script

set -o errexit

# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements.txt

# Create uploads directory
mkdir -p uploads

echo "Build completed successfully!"
