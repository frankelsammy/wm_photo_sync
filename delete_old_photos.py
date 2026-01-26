import os.path
from datetime import date, datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import os

wm_folder_id = '1zOaVshey7wahfCVGjRGhO7T-g5WsCmhJ'

def list_folders(parent_folder_id):
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # The file token.json stores the user's access and refresh tokens
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
            # Ensure we get a refresh token
            creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        folders = []
        page_token = None
        while True:
            response = service.files().list(
                q=f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
                spaces='drive',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token
            ).execute()

            folders.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return folders
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []  
def delete_old_photos(days_old):
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        parent_folders = list_folders(wm_folder_id)
        for folder in parent_folders:
            folder_id = folder['id']
            page_token = None
            print(f"Checking folder: {folder['name']}")
            while True:
                response = service.files().list(
                    q=f"'{folder_id}' in parents and trashed=false",
                    spaces='drive',
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                    fields='nextPageToken, files(id, name, createdTime)',
                    pageToken=page_token
                ).execute()

                for file in response.get('files', []):
                    print(f"Found file: {file['name']}")
                    # Convert string to a datetime object
                    date_obj = datetime.strptime(file['name'], "%Y-%m-%d")
                    age_days = (date.today() - date_obj.date()).days
                    if age_days > days_old:
                        print(f"Deleting file: {file['name']} (age: {age_days} days)")
                        service.files().delete(fileId=file['id']).execute()

                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        
    except HttpError as error:
        print(f'An error occurred: {error}')
if __name__ == "__main__":
    delete_old_photos(30)