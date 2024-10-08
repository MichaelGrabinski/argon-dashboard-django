!/bin/bash

# ----------------------
# Kudu Deployment Script
# ----------------------

# Enable error handling
set -e

# Helpers
echo() {
  builtin echo "[Deployment] $@"
}

# Change to the directory with your code
cd "$HOME/site/wwwroot"

# Activate the virtual environment
echo "Activating virtual environment..."
source antenv/bin/activate

# Install Python dependencies (optional, Azure may handle this)
echo "Installing Python packages..."
pip install -r requirements.txt

# Run Django migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Run makemigrations (optional, generally not recommended on production)
# echo "Running makemigrations..."
# python manage.py makemigrations

# Load initial data
echo "Loading initial data..."
python LoadCSV.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Deployment script completed successfully."