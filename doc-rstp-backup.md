RTSP Backup Manager
====================

Deskripsi
---------
RTSP Backup Manager adalah sistem yang digunakan untuk mengambil stream RTSP dari NVR/DVR secara otomatis dan menyimpannya dalam struktur folder terorganisir. Sistem ini dilengkapi dengan fitur:
1. Penyesuaian zona waktu dinamis (Wita/Wib).
2. Struktur folder berdasarkan tanggal dan nomor channel.
3. Log terstruktur untuk memantau status backup.
4. Pembersihan otomatis folder backup tertua jika kapasitas HDD penuh.

Struktur Direktori
------------------
### Lokasi Root Proyek
```
/home/abdullah/
├── rtsp/                      # Folder untuk proyek RTSP backup
│   ├── logs/                  # Folder log RTSP
│   ├── scripts/               # Script utama backup RTSP
│   ├── docker-compose.yml     # File docker-compose untuk RTSP
│   ├── Dockerfile             # File Docker untuk RTSP
│   ├── .env                   # Konfigurasi lingkungan RTSP
│
├── syslog/                    # Folder untuk proyek Syslog
│   ├── logs/                  # Folder log Syslog
│   ├── scripts/               # Script utama monitoring Syslog
│   ├── docker-compose.yml     # File docker-compose untuk Syslog
│   ├── Dockerfile             # File Docker untuk Syslog
│   ├── .env  
```

Konfigurasi
-----------
### File `.env`
Berikut adalah contoh konfigurasi `.env`:
```
# Pilih zona waktu sesuai lokasi:
# Untuk Jakarta:
TIMEZONE=Asia/Jakarta
# Untuk Makassar:
# TIMEZONE=Asia/Makassar

# Detail Login untuk RTSP:
RTSP_USERNAME=username          # Username untuk autentikasi RTSP
RTSP_PASSWORD=password             # Password untuk autentikasi RTSP

# IP RTSP NVR atau DVR:
RTSP_IP=192.168.1.1              # IP dari perangkat RTSP Anda

# Jumlah channel RTSP yang ingin di-backup:
CHANNELS=8                          # Contoh: 8 channel

# Folder output RTSP (container Docker):
RTSP_OUTPUT_DIR=/data               # Lokasi penyimpanan hasil backup di dalam container

# Folder TrueNAS (host):
BACKUP_DIR=/mnt/Backup/             # Lokasi backup di sistem host (TrueNAS)
```

Fitur
-----
1. **Struktur Folder Backup**
   - **Format Folder**: `/mnt/Backup/<Tanggal>/Channel <Nomor Channel>`
   - **Format File**: `<Jam-Menit-Detik>.mp4`
   - Contoh:
     ```
     /mnt/Backup/21-12-2024/Channel 1/08-15-30.mp4
     /mnt/Backup/21-12-2024/Channel 2/08-15-30.mp4
     ```

2. **Log Backup**
   - Format log mencakup waktu lokal (Wita/Wib), level log, dan pesan.
   - Contoh log:
     ```
     21-12-2024 08:15:00 Wita - INFO - Backup berhasil: /mnt/Backup/21-12-2024/Channel 1/08-15-30.mp4
     21-12-2024 08:16:00 Wita - ERROR - Backup gagal untuk channel 2. Exit status 1
     ```

3. **Pembersihan Otomatis**
   - Folder backup tertua akan dihapus jika penggunaan HDD melebihi 90%.

Langkah Instalasi
-----------------
### 1. Kloning Proyek
```
git clone https://github.com/babahdigital/rtsp-backup-manager.git
cd rtsp-backup-manager
```

### 2. Buat File `.env`
- Salin template dan sesuaikan:
```
cp .env.example .env
nano .env
```

### 3. Bangun dan Jalankan Container
- Dengan Docker Compose:
```
docker-compose up --build -d
```

Langkah Simulasi
----------------
1. Pastikan `.env` sudah dikonfigurasi.
2. Jalankan simulasi backup untuk channel tertentu:
   ```
   python3 scripts/backup_manager.py --channel 1
   ```
3. Periksa log di:
   ```
   /home/abdullah/rtsp-backup/logs/backup.log
   ```

Troubleshooting
---------------
### 1. Backup Gagal
- Periksa log di `logs/backup.log` untuk melihat pesan error.
- Pastikan URL RTSP, username, dan password sudah benar.

### 2. HDD Penuh
- Sistem akan otomatis menghapus folder tertua.
- Periksa log di `logs/hdd_monitor.log` untuk riwayat pembersihan.

### 3. Tidak Ada File di Folder Backup
- Pastikan konfigurasi `.env` sudah benar.
- Jalankan perintah berikut untuk memeriksa:
   ```
   docker logs <container_id>
   ```

Pengembangan dan Kontribusi
---------------------------
1. Untuk menambahkan fitur baru, pastikan mengikuti struktur proyek yang sudah ada.
2. Dokumentasi setiap perubahan wajib diperbarui di file `README.md`.

Jika ada pertanyaan lebih lanjut, silakan hubungi tim pengembang di GitHub atau melalui email resmi.
