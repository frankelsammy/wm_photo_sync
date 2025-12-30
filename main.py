import download_photos
import upload_to_google_drive

if __name__ == "__main__":
    results_dir = download_photos.download_todays_media()
    print("Finished downloading photos. Now uploading to Google Drive...")
    upload_to_google_drive.upload_photos(results_dir)
    print("Upload complete.")
