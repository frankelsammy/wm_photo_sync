import shutil
import sys
from datetime import date, timedelta
from enum import Enum

import download_photos
import upload_to_google_drive
class Mode(Enum):
    NORMAL = 0,
    RENDER = 1
if __name__ == "__main__":
    #delete photos from two days ago before downloading today's
    yesterday = date.today() - timedelta(2)
    shutil.rmtree("results/" + str(yesterday), ignore_errors=True)

    #Check if any locations were schedulued for service yesterday and we didn't download any photos for them
    mode = Mode.RENDER if len(sys.argv) > 1 and sys.argv[1] == "render" else Mode.NORMAL
    results_dir = download_photos.download_todays_media(mode)
    print("Finished downloading photos. Now uploading to Google Drive...")
    upload_to_google_drive.upload_photos(results_dir)
    print("Upload complete.")
