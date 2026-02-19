import shutil
import sys
from datetime import date, timedelta
from enum import Enum

import download_photos
import upload_to_google_drive
import delete_old_photos
import gmail
class Mode(Enum):
    NORMAL = 0,
    RENDER = 1
if __name__ == "__main__":
    #delete photos from two days ago before downloading today's
    old_dir = date.today() - timedelta(2)
    shutil.rmtree("results/" + str(old_dir), ignore_errors=True)

    mode = Mode.RENDER if len(sys.argv) > 1 and sys.argv[1] == "render" else Mode.NORMAL
    try:
        results_dir = download_photos.download_todays_media(mode)
        print("Finished downloading photos. Now uploading to Google Drive...")
        photos_uploaded = upload_to_google_drive.upload_photos(results_dir)
        print("Upload complete.")
        # Now delete old photos from Google Drive
        print("Deleting old photos from Google Drive...")
        deleted = delete_old_photos.delete_old_photos(days_old=30)
        gmail.send_email(f"WM Photo Sync completed successfully. {photos_uploaded} photos uploaded. {deleted} old photos deleted.")
    except Exception as e:
        print(f"An error occurred during download/upload: {e}")
        gmail.send_email(f"An error occurred during download/upload: {e}")
