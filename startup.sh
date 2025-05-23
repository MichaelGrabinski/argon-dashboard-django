#!/bin/sh
set -e

# 1) Add the system libraries WeasyPrint / PyGObject need
apt-get update
apt-get install -y --no-install-recommends \
    libglib2.0-0  \
    libgobject-2.0-0 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0

# 2) Hand control back to Gunicorn (replace «yourproject» if needed)
exec gunicorn yourproject.wsgi:application \
     --bind 0.0.0.0:${PORT:-8000} \
     --workers 4 --timeout 600
