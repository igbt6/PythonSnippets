import os
import sys
import re
import fileinput

"""useful script that modifies files in place """



'''# Recursive method, returns all file paths in  a given folder'''
def getAllFilePathsFromFolder(folder, listOfFilesPaths): 
    folderContent = os.listdir(folder)
    for item in folderContent:
        if os.path.isfile(os.path.join(folder, item)):
            listOfFilesPaths.append(os.path.join(folder, item))
        else:
            getAllFilePathsFromFolder(os.path.join(folder, item), listOfFilesPaths)
    return listOfFilesPaths

def modifyIncludePaths(rootFolderPath, folders):    
    folderPaths = [os.path.join(rootFolderPath, folder) for folder in folders]
    if( not (os.path.exists(rootFolderPath))):
        raise IOError("Such folder does not exist !!")
    filePaths =[]
    for rootFolderPath in folderPaths:
        getAllFilePathsFromFolder(rootFolderPath, filePaths) 
    filePaths = [path for path in filePaths if path.endswith(".c") or path.endswith(".h") ] #only .c and .h files
    
    for filePath in filePaths:
        with fileinput.FileInput(filePath, inplace=True) as file:
            for line in file:
                if line.find('"inc/') is not -1:
                    print(line.replace('"inc/', '"../inc/'), end="")
                elif line.find('"driverlib/') is not -1:
                    print(line.replace('"driverlib/', '"../driverlib/'), end="")
                elif line.find('"usblib/') is not -1:
                    print(line.replace('"usblib/', '"../usblib/'), end="")
                elif line.find('"utils/') is not -1:
                    print(line.replace('"utils/', '"../utils/'), end="")   
                else:
                    print(line, end="")

def main():
    folders =['driverLib', 'inc', 'usblib', 'utils']
    modifyIncludePaths(os.getcwd(), folders)    
    
        
if __name__ == '__main__':
    main()
 
