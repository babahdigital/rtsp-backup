#!/usr/bin/env bash
#
# -------------------------------------------------------------------------------
# Entrypoint untuk Docker Container
# -------------------------------------------------------------------------------
# - Meload file .env
# - Mengecek environment variable penting
# - Menjalankan loop tak terhingga untuk backup rekaman CCTV
# -------------------------------------------------------------------------------

# Aktifkan "strict mode" agar script berhenti jika terjadi error
set -Eeuo pipefail

# 1. Pastikan file .env ada
if [ ! -f /app/.env ]; then
    echo "File lingkungan (.env) tidak ditemukan. Pastikan file tersebut ada di /app/.env."
    exit 1
fi

# 2. Load environment variables (.env)
source /app/.env

# 3. Validasi variabel lingkungan yang diperlukan
REQUIRED_VARS=("RTSP_USERNAME" "RTSP_PASSWORD" "RTSP_IP" "BACKUP_DIR" "TIMEZONE" "VIDEO_DURATION" "CHANNELS" "RETRY_DELAY" "CONCURRENCY_LIMIT" "MAX_CAPACITY_PERCENT")
for VAR in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!VAR:-}" ]]; then
        echo "$(date '+%d-%m-%Y %H:%M:%S') - ERROR: Variabel lingkungan $VAR tidak ditemukan. Pastikan .env telah dikonfigurasi dengan benar."
        exit 1
    fi
done

# 4. Set timezone
export TZ="$TIMEZONE"
ln -snf "/usr/share/zoneinfo/$TIMEZONE" /etc/localtime && echo "$TIMEZONE" > /etc/timezone

# 5. Logging ke file (entrypoint.log) agar mudah memonitor
LOG_FILE="/app/logs/entrypoint.log"
mkdir -p /app/logs
exec > >(tee -a "$LOG_FILE") 2>&1

echo "$(date '+%d-%m-%Y %H:%M:%S') - INFO: Memulai entrypoint..."
echo "$(date '+%d-%m-%Y %H:%M:%S') - INFO: VIDEO_DURATION (durasi rekaman) = $VIDEO_DURATION detik."

# -------------------------------------------------------------------------------
# Fungsi: backup_channel
# - Digunakan untuk melakukan backup rekaman satu channel
# -------------------------------------------------------------------------------
backup_channel() {
    local CHANNEL=$1
    local URL="rtsp://$RTSP_USERNAME:$RTSP_PASSWORD@$RTSP_IP/streaming/channels/$CHANNEL"

    echo "$(date '+%d-%m-%Y %H:%M:%S') - INFO: Memulai backup untuk Channel ${CHANNEL} ..."
    python3 /app/scripts/backup_manager.py --channel "$CHANNEL" --url "$URL"
    local EXIT_CODE=$?

    if [ $EXIT_CODE -ne 0 ]; then
        echo "$(date '+%d-%m-%Y %H:%M:%S') - ERROR: Backup gagal untuk Channel ${CHANNEL} (exit code $EXIT_CODE)."
    else
        echo "$(date '+%d-%m-%Y %H:%M:%S') - INFO: Backup selesai untuk Channel ${CHANNEL}."
    fi
}

# 6. Baca variabel tambahan (CHANNELS, RETRY_DELAY, CONCURRENCY_LIMIT)
CHANNELS=${CHANNELS:-1}                   # default 1 jika tidak di-set
RETRY_DELAY=${RETRY_DELAY:-30}            # default 30 detik
CONCURRENCY_LIMIT=${CONCURRENCY_LIMIT:-0} # 0 artinya tak dibatasi

# 7. Loop tak terhingga untuk backup semua channel
while true; do
    echo "$(date '+%d-%m-%Y %H:%M:%S') - INFO: Memulai iterasi backup..."

    running_jobs=0

    # Loop untuk semua channel
    for (( CH=1; CH<=CHANNELS; CH++ )); do
        # Jalankan backup_channel secara background (&)
        backup_channel "$CH" &
        ((running_jobs++))

        # Jika ada concurrency limit, tunggu satu proses selesai jika melebihi limit
        if [ "$CONCURRENCY_LIMIT" -gt 0 ] && [ "$running_jobs" -ge "$CONCURRENCY_LIMIT" ]; then
            wait -n  # menunggu satu job selesai
            ((running_jobs--))
        fi
    done

    # Tunggu semua job background (backup) selesai
    wait

    echo "$(date '+%d-%m-%Y %H:%M:%S') - INFO: Semua channel selesai di-backup. Menunggu $RETRY_DELAY detik sebelum iterasi berikutnya..."
    sleep "$RETRY_DELAY"
done
