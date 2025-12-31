# wm_photo_sync

**Automated Photo Download and Upload Service**

`wm_photo_sync` is a Python automation tool developed for Negotiated Waste. It downloads photos from WasteManagement.com for scheduled locations, organizes them by date, and uploads them to Google Drive. The project automatically cleans up old photo directories, is containerized with Docker for reproducible deployments, and uses Playwright to handle browser-based downloads. Integration with the Google Drive API ensures secure and reliable storage of the photos.

---

## Project Structure

```
wm_photo_sync/
├── main.py                     # Main script
├── download_photos.py           # Handles downloading media
├── upload_to_google_drive.py    # Handles uploading to Google Drive
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker container definition
├── customer_id_map.py           # Customer mappings
└── results/                     # Temporary folder for downloaded photos
```


