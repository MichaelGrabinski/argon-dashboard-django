#!/bin/bash

# ----------------------
# Kudu Deployment Script
# ----------------------

# Enable error handling
set -e

# Helpers
echo() {
  builtin echo "[Deployment] $@"
}

# Update packages and install required system libraries
echo "Updating packages and installing required libraries..."
apt-get update
apt-get install -y libgirepository1.0-dev libglib2.0-dev
apt-get install -y libpango-1.0-0 libpango1.0-dev
apt-get install -y build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libcairo2-dev libpango1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Change to the directory with your code
cd "$HOME/site/wwwroot"

# Activate the virtual environment
echo "Activating virtual environment..."
source antenv/bin/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Run Django migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Load initial data
echo "Loading initial data..."
python LoadCSV.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Deployment script completed successfully."