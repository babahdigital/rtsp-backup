import os
import subprocess
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Logging configuration
LOG_FILE = "/app/logs/backup_manager.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Environment Variables
RTSP_USERNAME = os.getenv("RTSP_USERNAME", "admin")
RTSP_PASSWORD = os.getenv("RTSP_PASSWORD", "password")
RTSP_IP = os.getenv("RTSP_IP", "127.0.0.1")
BACKUP_DIR = os.getenv("BACKUP_DIR", "/data")
VIDEO_DURATION = int(os.getenv("VIDEO_DURATION", "300"))
CHANNELS = int(os.getenv("CHANNELS", "1"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
CONCURRENCY_LIMIT = int(os.getenv("CONCURRENCY_LIMIT", "8"))

if MAX_WORKERS <= 0:
    raise ValueError("MAX_WORKERS harus lebih besar dari 0.")
if CONCURRENCY_LIMIT < 1 or CONCURRENCY_LIMIT > CHANNELS:
    raise ValueError("CONCURRENCY_LIMIT harus berada di antara 1 dan jumlah CHANNELS.")

RTSP_SUBTYPE = os.getenv("RTSP_SUBTYPE", "1")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Makassar")
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "30"))

def get_current_time():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + (" WITA" if TIMEZONE == "Asia/Makassar" else " WIB")

def backup_channel(channel):
    try:
        rtsp_url = f"rtsp://{RTSP_USERNAME}:{RTSP_PASSWORD}@{RTSP_IP}:554/cam/realmonitor?channel={channel}&subtype={RTSP_SUBTYPE}"
        today = datetime.date.today().strftime("%d-%m-%Y")
        channel_dir = os.path.join(BACKUP_DIR, today, f"Channel {channel}")
        os.makedirs(channel_dir, exist_ok=True)
        output_file = os.path.join(channel_dir, f"{datetime.datetime.now().strftime('%H-%M-%S')}.mkv")

        logging.info(f"Memulai backup untuk channel={channel}, durasi={VIDEO_DURATION}s: {output_file}")
        subprocess.run(
            ["ffmpeg", "-fflags", "+genpts", "-i", rtsp_url, "-t", str(VIDEO_DURATION), "-c", "copy", output_file],
            check=True,
        )
        logging.info(f"Backup berhasil untuk channel={channel}: {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Backup gagal untuk channel={channel}: {e}")

def main():
    logging.info(f"Memulai proses backup dengan MAX_WORKERS={MAX_WORKERS} dan CONCURRENCY_LIMIT={CONCURRENCY_LIMIT}")
    channels_to_backup = range(1, CHANNELS + 1)

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for i in range(0, len(channels_to_backup), CONCURRENCY_LIMIT):
                subset = channels_to_backup[i:i + CONCURRENCY_LIMIT]
                logging.info(f"Memulai batch backup untuk channel: {list(subset)}")
                executor.map(backup_channel, subset)
                logging.info(f"Menunggu selama {RETRY_DELAY} detik sebelum batch berikutnya...")
                time.sleep(RETRY_DELAY)
    except KeyboardInterrupt:
        logging.info("Proses dihentikan oleh pengguna.")
    finally:
        logging.info("Backup Manager keluar dengan bersih.")

if __name__ == "__main__":
    main()