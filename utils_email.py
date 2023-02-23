from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.readonly']


# https://developers.google.com/gmail/api/quickstart/python
# for more details on this API

def send_email(recipient: str, subject: str, body_text: str, body_html: str):
    # get credentials
    creds = get_creds()
    service = build('gmail', 'v1', credentials=creds)

    # https://stackoverflow.com/questions/882712/send-html-emails-with-python
    # for sending HTML in emails

    # create email
    message = MIMEMultipart('alternative')
    message.attach(MIMEText(body_text, 'plain'))
    message.attach(MIMEText(body_html, 'html'))
    message['To'] = recipient
    message['From'] = 'nathanpham.me@gmail.com'
    message['Subject'] = subject

    # encoded message
    create_message = {
        'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
    }

    service.users().messages().send(userId="me", body=create_message).execute()


def get_creds():
    # get credentials
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds
