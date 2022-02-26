import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from mimetypes import guess_type as guess_mime_type
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']


def googledrive_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)


def upload_pic(drive_service, files, parent_id):
    for file in files:
        file_metadata = {'name': str(file),
                         'parents': [parent_id]}
        media = MediaFileUpload(file,
                                mimetype=guess_mime_type(file)[0])
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()


def create_folder(service, name):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': ''
    }
    folder_instagram = service.files().create(body=file_metadata,
                                                   fields='id').execute()
    return folder_instagram['id']


def get_id_of_folder(service, name_of_folder):
    page_token = None
    while True:
        response = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name = '{name_of_folder}'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            if file['name'] == name_of_folder:
                return file['id']
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            return create_folder(service, name_of_folder)
