# ——— Base OS + Nginx + Python ——————————————————————————
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ——— Project files ———————————————————————————————————————
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ——— Nginx reverse-proxy rules ————————————————————————
COPY infra/nginx.conf /etc/nginx/conf.d/default.conf

# ——— Expose just one port (Azure will send all traffic here) —
EXPOSE 80

# ——— Launch Gunicorn in the background then Nginx  —————
CMD gunicorn myproject.wsgi:application \
        --bind 127.0.0.1:8000 --workers 4 & \
    nginx -g "daemon off;"



# FROM python:3.9

#COPY . .

# set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

# install python dependencies
#RUN pip install --upgrade pip
#RUN pip install --no-cache-dir -r requirements.txt

# running migrations
#RUN python manage.py migrate

# gunicorn
#CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
