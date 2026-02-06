import os.path
import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file sammy-token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_service():
    """Helper to handle authentication and return the Gmail service object."""
    creds = None
    # Look for token in the same directory as this script
    token_path = os.path.join(os.path.dirname(__file__), "token-sammy.json")
    creds_path = os.path.join(os.path.dirname(__file__), "credentials.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    
    return build("gmail", "v1", credentials=creds)

def send_email(message_content):
  try:
    # Call the Gmail API
    service = get_gmail_service()
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
    return None
  finally:
    service.close()

  return sent_message["id"]

def delete_email(message_id):
    """
    Moves an email to the trash based on the provided ID.
    """
    try:
        service = get_gmail_service()
        # .trash() moves it to the bin. .delete() wipes it permanently.
        service.users().messages().trash(userId="me", id=message_id).execute()
        print(f"Successfully moved message {message_id} to trash.")
        return True
    except HttpError as error:
        print(f"An error occurred during deletion: {error}")
        return False
    finally:
       service.close()
  
if __name__ == "__main__":
  # send_email("This is a test email sent from Python!")
  delete_email("19c30b6b09dd9243")