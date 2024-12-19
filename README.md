# Babah Digital
# CCTV Backup Agent

This project provides a lightweight Python-based agent for automating CCTV backups. The agent captures video streams and stores them in a structured format, making retrieval and management simple and efficient.

## Features
- Automated backups of CCTV streams.
- File naming based on timestamp (dd-MM-yyyy_HH-MM-SS).
- Configurable using JSON files.
- Log rotation for efficient disk usage.
- Systemd integration for automation.

## Project Structure
cctv-backup-agent/ ├── backup/ │ ├── main.py # Backup script │ ├── config.json # Configuration file │ ├── requirements.txt # Python dependencies ├── tests/ │ ├── test_main.py # Unit tests ├── .gitignore # Ignored files ├── README.md # Project documentation

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/cctv-backup-agent.git
   cd cctv-backup-agent
   
2. Set up a Python virtual environment and install dependencies:
   python3 -m venv env
   source env/bin/activate
   pip install -r backup/requirements.txt

3. Usage
   Run the script manually
   Use the following command to run the backup script manually:
   python backup/main.py

Automate using Systemd
  1. Create a systemd service file:
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
  
  2. Enable and start the service:
        sudo systemctl daemon-reload
        sudo systemctl enable cctv-backup.service
        sudo systemctl start cctv-backup.service
        
        Testing
        Unit Tests
        Run tests using pytest:
        pytest tests/

Manual Testing
Verify backups by running:
python backup/main.py

Log Rotation
To configure log rotation, add the following configuration to /etc/logrotate.d/cctv-backup:
    /mnt/backup/cctv/*.mp4 {
        daily
        rotate 7
        compress
        missingok
        notifempty
    }

Future Enhancements
Add more robust error handling for stream interruptions.
Support multiple CCTV streams in parallel.
Centralize configuration management with a single YAML/JSON file.
   

