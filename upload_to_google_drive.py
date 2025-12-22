import os.path
from datetime import date

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

today = date.today()
today_str = today.strftime("%Y-%m-%d")
def upload_photos(results_dir):
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)

    folder_name = "WM Photos"

    # Check if folder exists
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])

    if files:
        # Folder exists
        wm_folder = files[0]
        print(f"Folder already exists: {wm_folder['id']}")
    else:
        # Folder doesn't exist, create it
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        wm_folder = service.files().create(body=file_metadata, fields="id, name").execute()
        print(f"Folder created: {wm_folder['id']}")

    path = results_dir
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            # Check if the folder already exists
            query = f"mimeType='application/vnd.google-apps.folder' and name='{dir}' and '{wm_folder['id']}' in parents and trashed=false"
            response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = response.get('files', [])
            if files:
                folder_id = files[0]['id']
            else:
              # Create the folder
              folder_metadata = {
                  "name": dir,
                  "parents": [wm_folder["id"]],
                  "mimeType": "application/vnd.google-apps.folder"
              }
              folder = (
                  service.files()
                  .create(body=folder_metadata, fields="id, name")
                  .execute()
              )
              folder_id = folder["id"]
            
            # Create folder for today's uploads
            
            # Check if today's folder exists
            query = f"mimeType='application/vnd.google-apps.folder' and name='{today_str}' and '{folder_id}' in parents and trashed=false"
            response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = response.get('files', [])

            if files:
                # Folder exists
                today_folder = files[0]
                print(f"Today's folder already exists: {today_folder['id']}")
            else:
                # Folder doesn't exist, create it
                today_metadata = {
                    "name": today_str,
                    "parents": [folder_id],
                    "mimeType": "application/vnd.google-apps.folder"
                }
                today_folder = service.files().create(body=today_metadata, fields="id, name").execute()
                print(f"Today's folder created: {today_folder['id']}")

            dir_path = os.path.join(root, dir)

            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)

                if os.path.isfile(file_path):
                    media = MediaFileUpload(file_path, resumable=True)
                
                uploaded_file = service.files().create(
                    body={"name": filename, "parents": [today_folder["id"]]},
                    media_body=media,
                    fields="id, name"
                ).execute()
                print(f"Uploaded file '{uploaded_file['name']}' with ID {uploaded_file['id']}")


  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None
  

    


if __name__ == "__main__":
  upload_photos("results/2025-12-22")