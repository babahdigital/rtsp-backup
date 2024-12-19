# Babah Digital
# CCTV Backup Agent

**CCTV Backup Agent** adalah proyek berbasis Python yang dirancang untuk mengotomatisasi proses pencadangan rekaman CCTV. Sistem ini dirancang agar ringan, mudah digunakan, dan dapat diandalkan untuk menyimpan rekaman video CCTV secara terstruktur dengan nama file berdasarkan waktu, mendukung pengelolaan file secara efisien, dan integrasi dengan sistem otomatis (systemd).

---

## **Fitur Utama**
- **Pencadangan Otomatis:** Mendukung pencadangan rekaman CCTV secara terjadwal.
- **Penamaan File Berdasarkan Waktu:** Format nama file menggunakan `dd-MM-yyyy_HH-MM-SS` untuk mempermudah pengelolaan.
- **Integrasi Systemd:** Mendukung otomatisasi penuh menggunakan layanan systemd.
- **Rotasi Log:** Mengoptimalkan penggunaan disk dengan konfigurasi log rotation.
- **Konfigurasi Sederhana:** Menggunakan file JSON untuk mempermudah pengaturan.

---

## Project Structure
```bash
cctv-backup-agent/
├── backup/
│   ├── main.py        # Skrip utama untuk pencadangan
│   ├── config.json    # File konfigurasi
│   ├── requirements.txt # Daftar dependensi Python
├── tests/
│   ├── test_main.py   # Unit testing
├── .gitignore         # Daftar file yang diabaikan Git
├── README.md          # Dokumentasi proyek
└── LICENSE            # Lisensi proyek
```
---

## **Instalasi**

1. Clone Repository
   Clone repository ini ke perangkat Anda:
   ```bash
   git clone https://github.com/yourusername/cctv-backup-agent.git
   cd cctv-backup-agent
   ```
2. Setup Lingkungan Virtual Python
   Buat virtual environment untuk Python dan install dependensi:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install --upgrade pip
   pip install -r backup/requirements.txt
   ```

## **Cara Penggunaan**
Menjalankan Script Secara Manual
Gunakan perintah berikut untuk menjalankan pencadangan secara manual:
```bash
python backup/main.py
```

## **Otomatisasi Menggunakan Systemd**
1. Buat file layanan systemd:
 ```ini
   [Unit]
   Description=CCTV Backup Service
   After=network.target
   
   [Service]
   ExecStart=/path/to/env/bin/python /path/to/cctv-backup-agent/backup/main.py
   Restart=always
   User=your-username
   Group=your-group
   WorkingDirectory=/path/to/cctv-backup-agent

   [Install]
   WantedBy=multi-user.target
```
2. Aktifkan dan jalankan layanan:
```bash
   sudo systemctl daemon-reload
   sudo systemctl enable cctv-backup.service
   sudo systemctl start cctv-backup.service
```

Testing
Unit Testing
Jalankan pengujian menggunakan pytest:
```bash
pytest tests/
```
Pengujian Manual
Jalankan script pencadangan secara manual:
```bash
python backup/main.py
```
Periksa direktori pencadangan `(/mnt/backup/cctv)` untuk memastikan file dicadangkan dengan benar.
```ini
/mnt/backup/cctv/*.mp4 {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```
Rencana Pengembangan
Menambahkan penanganan error yang lebih robust untuk gangguan aliran video.
Mendukung pencadangan paralel untuk banyak CCTV.
Menggunakan format konfigurasi YAML atau JSON terpusat.

Lisensi
Proyek ini dilisensikan di bawah MIT License. Silakan lihat file LICENSE untuk detail lebih lanjut.
