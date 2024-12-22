#!/usr/bin/env bash

# Aktifkan mode error handling
set -e

# Pastikan semua environment variables telah dimuat
source /app/.env

# Jalankan monitoring HDD di background
echo "$(date '+%Y-%m-%d %H:%M:%S') - INFO: Memulai HDD monitoring..."
python3 /app/scripts/hdd_monitor.py &

# Jalankan Flask untuk health check di background
echo "$(date '+%Y-%m-%d %H:%M:%S') - INFO: Memulai Flask untuk health check..."
python3 /app/scripts/health_check.py &

# Jalankan loop backup
echo "$(date '+%Y-%m-%d %H:%M:%S') - INFO: Memulai proses backup..."
while true; do
    python3 /app/scripts/backup_manager.py
    echo "$(date '+%Y-%m-%d %H:%M:%S') - INFO: Menunggu selama ${RETRY_DELAY} detik sebelum backup berikutnya..."
    sleep "${RETRY_DELAY:-30}"
done
