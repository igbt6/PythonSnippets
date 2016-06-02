from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import io
import apiclient
from apiclient.http import MediaIoBaseDownload



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GoogleDriveManager'


def get_credentials():
    '''Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    '''
    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'google_drive_manager.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def download_file(filename):
    credentials = get_credentials()
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http_auth)

    results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
    
    file_id = '0B0zxuHK9yGdHbml3ZUMtZThrVUU'
    request = service.files().get_media(fileId=file_id)
    #fh = io.BytesIO()
    fh = io.FileIO('aaaa', 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
        
if __name__ == '__main__':
    main()