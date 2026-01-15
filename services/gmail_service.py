import base64
import pickle
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

TOKEN_PATH = "token_gmail.pickle"
CREDENTIALS_PATH = "credentials.json"

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

# -----------------------------
# Mail Gönderme Fonksiyonu
# -----------------------------
def send_email(to, subject, body, attachments=None):
    """
    to: str, mail adresi
    subject: str
    body: str, HTML veya plain text
    attachments: list of tuple (filename, bytes)
    """
    service = get_gmail_service()
    msg = MIMEMultipart()
    msg['to'] = to
    msg['subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # PDF ekleri
    if attachments:
        for filename, file_bytes in attachments:
            part = MIMEApplication(file_bytes, Name=filename)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(part)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {'raw': raw}
    sent = service.users().messages().send(userId="me", body=message).execute()
    return sent
