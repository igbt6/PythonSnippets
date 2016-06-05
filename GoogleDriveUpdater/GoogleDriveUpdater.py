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
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GoogleDriveManager'
FOLDER_TO_BE_SYNCED_PATH= 'L:\GOOGLE_DRIVE_SYNCER_TEST_FOLDER'

class GoogleDriveSynchronizer():

    def __init__(self,root_folder_name):
        self._root_folder= root_folder_name
        self._credentials = self.get_credentials()
        self._http_auth = self._credentials.authorize(httplib2.Http())
        self._service = discovery.build('drive', 'v3', http=self._http_auth)
        #self.check_if_file_exist_create_new_one(self._root_folder)
        
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
            return False
        page_token = None
        while True:
            response = self._service.files().list(q="name = '%s'"%file_name,
                                                 spaces='drive',fields='nextPageToken, files(id, name)',
                                                 pageToken=page_token).execute()
            for file in response.get('files', []):
                print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                return file.get('id')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                return False;
        
    def check_if_file_exist_create_new_one(self,file_name,parent_id=None):
        id = self.find_folder_or_file_by_name(file_name)
        if self.find_folder_or_file_by_name(file_name):
            print(file_name + " exists")
        else:
            print(file_name + " does not exist")
            id=self.create_new_folder(file_name,parent_id)
        return id
        
    
    def list_all_files_in_main_folder(self):
        results = self._service.files().list().execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))
        
    def create_new_folder(self,folder_name,parent_folders_ids:list =None):
        file_metadata = {
            'name' : folder_name,
            'mimeType' : 'application/vnd.google-apps.folder',
            'parents': parent_folders_ids
        }
        file = self._service.files().create(body=file_metadata, fields='id').execute()
        print('Created Folder ID: %s' % file.get('id'))
        return file.get('id')
    
    def insert_file_in_folder(self,file_name,path,parent_folders_ids:list,file_mime_type=None):
        file_metadata = {
          'name' : file_name,
          'parents': parent_folders_ids
        }
        media = MediaFileUpload(path,
                                mimetype=file_mime_type,  # if None, it will be guessed 
                                resumable=True)
        file = self._service.files().create(body=file_metadata,media_body=media,fields='id').execute()
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
        self._files={}
        self._list_all_filepaths()
        
    def _list_all_filepaths(self):
        #print(os.listdir(self._root_path))
        for file_path in os.listdir(self._root_path):
            if os.path.isfile(os.path.join(self._root_path,file_path)):
                #print(os.path.join(self._root_path,file)) #left files
                pass
            else:
                self._files[file_path]={"PATH":os.path.join(self._root_path,file_path)}
        #print(self._files) 
        for name,dataDict in self._files.items():
            folders_set=set([])
            files_set= set([])
            for root_dir, subdirs, files in os.walk(dataDict["PATH"]):
                #print([subdir.encode('utf8') for subdir in subdirs])
                #print([file.encode('utf8') for file in files])
                folders_set.add(root_dir)
                #print(root_dir)
                for file in files:
                        files_set.add(os.path.join(root_dir,file))
                for subdir in subdirs:
                    folders_set.add(os.path.join(root_dir,subdir))
                    for file in files:
                        files_set.add(os.path.join(root_dir,file))

            with open("result.txt","a") as f:
                f.write("\n--------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write("----------------------NAME---------------------------\n")
                f.write(name)
                f.write('\n')
                
                f.write("\n--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                f.write("--------------------FOLDERS---------------------------\n")
                for i in sorted(folders_set, key=len):
                    f.write(i)
                    f.write('\n')
                f.write("\n--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                f.write("--------------------FILES---------------------------\n")
                for i in files_set:
                    f.write(i)
                    f.write('\n')
            self._files[name]["FOLDERS"]=sorted(folders_set, key=len)
            self._files[name]["FILES"]=list(files_set)
            # print("\n--------------------PATH---------------------------\n")
            # print(self._files[name]["PATH"])
            # print("\n--------------------FOLDERS---------------------------\n")
            # print(self._files[name]["FOLDERS"])
            # print("\n--------------------FILES---------------------------\n")
            # print(self._files[name]["FILES"])
            #break
     
    def extract_folder_name_from_path(self,folder_path):
        m =re.search(r'\\(\w*)$',folder_path)
        if m:
            return m.group(1)
        else:
            raise ValueError("Incorrect folder_path %s"%folder_path)
            
    @property
    def files(self):
        return self._files
    
    @property
    def root_folder_path(self):
        return self._root_path
        
        
        
class GoogleDriveFile():
    def __init__(file_name):
        self.file_name= file_name
        self.file_id =None
        self.parent_folder_id=''
    
        
if __name__ == '__main__':
    file_folder = FilesFolder(os.path.join(FOLDER_TO_BE_SYNCED_PATH))
    google_drive_syncer= GoogleDriveSynchronizer(file_folder.extract_folder_name_from_path(file_folder.root_folder_path))  
    #google_drive_syncer.list_all_files_in_main_folder()
    #for name, data in file_folder.files.items():
        #google_drive_syncer.check_if_file_exist_create_new_one(name)
    # TEST1
    id=google_drive_syncer.check_if_file_exist_create_new_one("TEST_FOLDER")
    google_drive_syncer.insert_file_in_folder("TestFolderFile.txt",os.path.join(FOLDER_TO_BE_SYNCED_PATH,"cowsay.txt"),[id])
    #0B0zxuHK9yGdHSC15aG5FWExBNm8
    #id=google_drive_syncer.check_if_file_exist_create_new_one("TEST_SUB_FOLDER",["0B0zxuHK9yGdHSC15aG5FWExBNm8"])
    id=google_drive_syncer.check_if_file_exist_create_new_one("TEST_SUB_FOLDER",[id])
    google_drive_syncer.insert_file_in_folder("TestSubFolderFile.txt",os.path.join(FOLDER_TO_BE_SYNCED_PATH,"cowsay.txt"),[id])