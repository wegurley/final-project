# Dockerfile
FROM python:3.11-slim

# metadata
LABEL maintainer="Your Name <you@example.com>" \
      version="0.1" \
      description="Mini Stats API - Upload based"

# system deps for matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# create app dir
WORKDIR /app

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy source
COPY src /app/src
WORKDIR /app/src

# expose port
EXPOSE 8080

# default envs (can be overridden)
ENV PORT=8080
ENV FLASK_ENV=production

# use gunicorn for a more production-like server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers", "1", "--threads", "4", "--timeout", "120"]

