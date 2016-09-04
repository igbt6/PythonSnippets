import sys
import os
import shutil
import argparse
import subprocess

FZD_PENDRIVE_PATH = "D://"
_7ZIP_PATH= os.path.join("C://Program Files//7-Zip//7z.exe")
    
def copyFile(srcPath,destPath):
    fullSrcPath = os.path.abspath(srcPath)
    if(not os.path.isfile(fullSrcPath)):
        print("File: "+ srcPath + "does not exist under given path")
        return False
    shutil.copy(fullSrcPath, os.path.join(destPath,srcPath))
    return True

def unzipFile(filePath,destPath):
    print(" --- unzipping... ---")
    try:
        cmd =[_7ZIP_PATH, 'x', filePath, '-aoa', '-o'+destPath] #-aoa:     overwrite all existing files
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print('[ERRROR] '+str(e.output))
        print('[ERRROR] '+" Return code = "+str(e.returncode))
    except subprocess.TimeoutExpired as e:
        print('[ERRROR] '+"TimeoutExpired "+str(e))
        
def zipFile(filePath,destPath):
    print(" --- zipping... ---")
    try:
        cmd =[_7ZIP_PATH, 'a', '-tzip', destPath, filePath]
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print('[ERRROR] '+str(e.output))
        print('[ERRROR] '+" Return code = "+str(e.returncode))
    except subprocess.TimeoutExpired as e:
        print('[ERRROR] '+"TimeoutExpired "+str(e))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-zip","--zip", help="zips the file/s",action="store_true")
    parser.add_argument("-unzip","--unzip", help="unzips the file/s",action="store_true")
    args = parser.parse_args()
    
    if args.gen2 or args.gen3: 
        zipName="test.zip"
        if args.zip:
            if copyFile(zipName,FZD_PENDRIVE_PATH):
                unzipFile(os.path.join(FZD_PENDRIVE_PATH,zipName),FZD_PENDRIVE_PATH)
        elif args.unzip:
            zipFile("Copy-file-and-zip_unzip_with7z.py",zipName)  
          
    else:
        print("Please put an argument [-gen2,-gen3]")
