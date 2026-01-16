import io
import pickle
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import current_year_month, SHARED_DRIVE_ID, BORDRO_ROOT_FOLDER_ID

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def find_folder(service, parent_id, folder_name):
    query = (
        f"name='{folder_name}' and "
        f"mimeType='application/vnd.google-apps.folder'"
    )

    # Shared Drive root için parents filtresi kullanma
    if parent_id != SHARED_DRIVE_ID:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(
        q=query,
        corpora="drive",
        driveId=SHARED_DRIVE_ID,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        fields="files(id, name)"
    ).execute()

    folders = results.get("files", [])
    return folders[0]["id"] if folders else None

def get_current_month_pdfs():
    service = get_drive_service()
    year, month = current_year_month()

    year_folder = find_folder(service, BORDRO_ROOT_FOLDER_ID, str(year))
    if not year_folder:
        raise Exception(f"{year} klasörü bulunamadı")

    month_folder = find_folder(service, year_folder, month)
    if not month_folder:
        raise Exception(f"{month} klasörü bulunamadı")

    results = service.files().list(
        q=(
            f"'{month_folder}' in parents "
            f"and mimeType='application/pdf' "
            f"and trashed = false"
        ),
        corpora='drive',
        driveId=SHARED_DRIVE_ID,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        fields="files(id, name)"
    ).execute()

    return {f["name"]: f["id"] for f in results.get("files", [])}

def download_pdf(file_id):
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    fh.seek(0)
    return fh.read()
