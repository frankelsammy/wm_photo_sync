from datetime import date, timedelta
import shutil

import download_photos
import upload_to_google_drive

if __name__ == "__main__":
    #delete yesterday's photos before downloading today's
    yesterday = date.today() - timedelta(1)
    shutil.rmtree("results/" + str(yesterday), ignore_errors=True)

    results_dir = download_photos.download_todays_media()
    print("Finished downloading photos. Now uploading to Google Drive...")
    upload_to_google_drive.upload_photos(results_dir)
    print("Upload complete.")
