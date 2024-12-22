import os
import shutil
import time
import logging

# Konfigurasi Logging
logging.basicConfig(
    filename="/app/logs/hdd_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Variabel lingkungan
BACKUP_DIR = os.getenv("BACKUP_DIR", "/mnt/Data/Backup")
MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", "60"))  # Interval monitoring dalam detik
MAX_CAPACITY_PERCENT = int(os.getenv("MAX_CAPACITY_PERCENT", "90"))  # Threshold kapasitas maksimum

def get_disk_usage(directory):
    """Menghitung penggunaan disk."""
    total, used, free = shutil.disk_usage(directory)
    usage_percent = (used / total) * 100
    return total, used, free, usage_percent

def format_size(size):
    """Format ukuran menjadi human-readable (KiB, MiB, GiB, TiB)."""
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TiB"

def delete_oldest_files(directory, threshold_percent):
    """Hapus file tertua jika penggunaan disk melewati ambang batas."""
    total, used, free, usage_percent = get_disk_usage(directory)
    initial_usage = usage_percent  # Simpan nilai awal untuk log

    if usage_percent < threshold_percent:
        logging.info(f"Disk usage {usage_percent:.2f}% belum mencapai threshold {threshold_percent}%. Tidak ada file yang dihapus.")
        return

    logging.warning(f"Disk usage {usage_percent:.2f}% melewati threshold {threshold_percent}%. Mulai proses rotasi.")

    files = sorted(
        (os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames),
        key=os.path.getmtime
    )

    while usage_percent > threshold_percent and files:
        oldest_file = files.pop(0)
        try:
            os.remove(oldest_file)
            relative_path = os.path.relpath(oldest_file, BACKUP_DIR)
            logging.info(f"Menghapus file: /Backup/{relative_path}")
        except Exception as e:
            logging.error(f"Gagal menghapus file {oldest_file}: {e}")
        
        # Re-check disk usage
        total, used, free, usage_percent = get_disk_usage(directory)

        # Hentikan jika disk usage di bawah threshold
        if usage_percent <= threshold_percent:
            logging.info(f"Proses rotasi selesai. Disk usage sekarang: {usage_percent:.2f}%")
            break

    if usage_percent > threshold_percent:
        logging.warning(f"Proses rotasi tidak cukup. Disk usage tetap: {usage_percent:.2f}%")

def monitor_disk_usage():
    """Monitoring disk dan menjalankan rotasi jika diperlukan."""
    try:
        while True:
            logging.info("Memulai HDD monitoring untuk NAS...")
            total, used, free, usage_percent = get_disk_usage(BACKUP_DIR)
            logging.info(
                f"Disk Usage: {usage_percent:.2f}% | Total: {format_size(total)} | Used: {format_size(used)} | Free: {format_size(free)}"
            )

            if usage_percent >= MAX_CAPACITY_PERCENT:
                delete_oldest_files(BACKUP_DIR, MAX_CAPACITY_PERCENT - 5)  # Rotasi hingga penggunaan < threshold

            time.sleep(MONITOR_INTERVAL)
    except KeyboardInterrupt:
        logging.info("HDD Monitoring dihentikan oleh pengguna.")
        print("HDD Monitoring dihentikan dengan bersih.")

if __name__ == "__main__":
    monitor_disk_usage()