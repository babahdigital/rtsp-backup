# Gunakan base image Python slim
FROM python:3.11-slim

# Install system dependencies termasuk FFmpeg
RUN apt-get update && apt-get install -y ffmpeg libavcodec-extra curl && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Buat direktori kerja /app di dalam container
WORKDIR /app

# Salin file requirements terlebih dahulu agar layer cache pip tidak sering invalidated
COPY scripts/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Salin health_check.py ke dalam container
COPY scripts/health_check.py /app/scripts/health_check.py

# Salin folder scripts ke dalam /app/scripts
COPY scripts/ /app/scripts/

# Salin entrypoint.sh ke direktori kerja dalam container
COPY scripts/entrypoint.sh /app/entrypoint.sh

# Salin file .env
COPY .env /app/.env

RUN mkdir -p /app/logs

# Beri izin eksekusi pada entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# ENTRYPOINT menjalankan script /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
