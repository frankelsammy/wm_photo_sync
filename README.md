# wm_photo_sync

**Automated Photo Download and Upload Service**

`wm_photo_sync` is a Python automation tool that downloads photos from WasteManagement.com for scheduled locations, organizes them by date, uploads them to Google Drive, and automatically cleans up old data.

The service is designed to run unattended and handle the full lifecycle of photo ingestion, storage, notification, and retention.

---

## Overview

On each run, the service:

* Downloads daily photos using browser automation
* Stores photos locally in date-based directories
* Uploads photos to Google Drive
* Sends email notifications on success or failure
* Deletes old local photo directories
* Removes expired photos from Google Drive based on a retention policy

A lightweight render/preview mode is also supported.

---

## Project Structure

```
wm_photo_sync/
├── main.py                        # Orchestrates the full workflow
├── download_photos.py            # Downloads photos via browser automation
├── upload_to_google_drive.py     # Uploads files to Google Drive
├── delete_old_photos.py          # Deletes old photos from Google Drive
├── send_email.py                 # Email notifications
├── customer_id_map.py            # Customer/location mappings
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container definition
└── results/                     # Temporary local photo storage
```

---

## Technologies

* Python
* Playwright
* Google Drive API
* Docker
