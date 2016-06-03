from __future__ import print_function
import httplib2
import os
import sys
import re
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import io
import apiclient
from apiclient.http import MediaIoBaseDownload


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GoogleDriveManager'
FOLDER_TO_BE_SYNCED_PATH= 'L:\EBOOKS'

class GoogleDriveSynchronizer():

    def __init__(self):
        self._credentials = self.get_credentials()
        self._http_auth = self._credentials.authorize(httplib2.Http())
        self._service = discovery.build('drive', 'v3', http=self._http_auth)
        
    def get_credentials(self):
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
        credential_path = os.path.join(credential_dir,'google_drive_manager.json')
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
       
    def find_folder_or_file_by_name(self,file_name):
        if(file_name ==None or len(file_name)==0):
            return
        page_token = None
        while True:
            response = self._service.files().list(q="name = '%s'"%file_name,
                                                 spaces='drive',fields='nextPageToken, files(id, name)',
                                                 pageToken=page_token).execute()
            for file in response.get('files', []):
                print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break;
        
        
    def list_all_files_in_folder(self):
        results = self._service.files().list().execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))
        
    def create_new_folder(self,folder_name):
        file_metadata = {
            'name' : folder_name,
            'mimeType' : 'application/vnd.google-apps.folder'
        }
        file = self._service.files().create(body=file_metadata, fields='id').execute()
        print('Created Folder ID: %s' % file.get('id'))
    
    def insert_file_in_folder(self,folder_id,file_name,mime_type):
        file_metadata = {
          'name' : 'photo.jpg',
          'parents': [ folder_id ]
        }
        media = MediaFileUpload('files/file_name',
                                mimetype='image/jpeg', #TODO
                                resumable=True)
        file = drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()
        print('File ID: %s' % file.get('id'))
        
    def main():
        results = self._service.files().list(pageSize=10,fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))
        
        file_id = '0B0zxuHK9yGdHbml3ZUMtZThrVUU'
        request = self._service.files().get_media(fileId=file_id)
        #fh = io.BytesIO()
        fh = io.FileIO('aaaa', 'wb')
        # downloader = MediaIoBaseDownload(fh, request)
        # done = False
        # while done is False:
            # status, done = downloader.next_chunk()
            # print("Download %d%%." % int(status.progress() * 100))

class FilesFolder():

    def __init__(self, main_folder_path):
        if not os.path.exists(main_folder_path):
            raise IOError("incorrect path of your main folder!")       
        self._root_path=main_folder_path 
        self._files=[]
        #TESTS
        self._list_all_filepaths()
        
    def _list_all_filepaths(self):
        modified_root_path= self._root_path.replace("\\","\\\\")
        for root_dir, subdirs, files in os.walk(self._root_path):
            if re.match(r'%s(\\\w*)$'%modified_root_path,root_dir):
                print("AFTER "+root_dir)
                print([subdir.encode('utf8') for subdir in subdirs])
                print([file.encode('utf8') for file in files])
                # self._files.append(file)

        
if __name__ == '__main__':
    google_drive_syncer= GoogleDriveSynchronizer()
    #file_folder = FilesFolder(os.path.join(FOLDER_TO_BE_SYNCED_PATH))
    #google_drive_syncer.list_all_files_in_folder()
    google_drive_syncer.find_folder_or_file_by_name("EMBEDDED")