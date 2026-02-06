from curses import error
import os.path

import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]



def send_email(message_content):
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token-sammy.json"):
    creds = Credentials.from_authorized_user_file("token-sammy.json", SCOPES)
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
    with open("token-sammy.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content(message_content)

    message["To"] = "frankelsammy31@gmail.com"
    message["From"] = "frankelsammy31@gmail.com"
    message["Subject"] = "WM Photo Sync Status"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"message": {"raw": encoded_message}}
    # pylint: disable=E1101
    sent_message = (
    service.users()
    .messages()
    .send(userId="me", body={"raw": encoded_message})
    .execute()
  )

    print(f'Sent message id: {sent_message["id"]}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    create_message = None

  return create_message
if __name__ == "__main__":
  send_email("This is a test email sent from Python!")