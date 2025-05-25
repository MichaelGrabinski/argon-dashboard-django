# ------------- Base OS with Python + Nginx -------------
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------- Project code -----------------------------
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ------------- Nginx reverse-proxy ----------------------
COPY infra/nginx.conf /etc/nginx/conf.d/default.conf

# ------------- Expose & launch --------------------------
EXPOSE 80
CMD gunicorn apps.wsgi:application \          # ← replace “myproject”
        --bind 127.0.0.1:8000 --workers 4 & \
    nginx -g "daemon off;"
