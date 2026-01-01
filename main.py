from datetime import date, timedelta
import shutil
import sys

import download_photos
import upload_to_google_drive

if __name__ == "__main__":
    #delete photos from two days ago before downloading today's
    yesterday = date.today() - timedelta(2)
    shutil.rmtree("results/" + str(yesterday), ignore_errors=True)

    #Check if any locations were schedulued for service yesterday and we didn't download any photos for them
    mode = sys.argv[1] if len(sys.argv) > 1 else 'normal'
    results_dir = download_photos.download_todays_media(mode)
    print("Finished downloading photos. Now uploading to Google Drive...")
    upload_to_google_drive.upload_photos(results_dir)
    print("Upload complete.")
