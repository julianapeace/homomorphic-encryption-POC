'''
Created on Aug 18, 2018
@author: zhaosong
https://www.dev2qa.com/python-check-if-file-exists-and-create-example/
'''

import os, stat
import pathlib

# Check file/folder existence by os.path.exists method.
def checkFileExistByOSPath(file_path):

    ret = False
    # If this file object exist.
    if(os.path.exists(file_path)):
        ret = True
        print(file_path + " exist.")
        # If this is a file.
        if(os.path.isfile(file_path)):
            print(" and it is a file.")
        # This is a directory.    
        else:
            print(" and it is a directory.")
    else:
        ret = False
        print(file_path + " do not exist.")
        
    return ret

# Check file/folder existence by exception.         
def checkFileExistByException(file_path):
    ret = True
    try:
        # Open file object.
        file_object = open(file_path, 'r')
        # Read entire file content data.
        file_data = file_object.read()
        print(file_path + " exist. It's data : " + file_data)
    except FileNotFoundError:
        ret = False
        print(file_path + " do not exist.")
    except IOError:
        ret = False
        print(file_path + " can not be read. ")    
    except PermissionError:
        ret = False
        print("Do not have permission to read file " + file_path)

    return ret

# Check file/folder existence by pathlib.         
def checkFileExistByPathlib(file_path):
    ret = True
        
    # Create path lib object.
    pl = pathlib.Path(file_path)
    
    # Check whether the path lib exist or not.
    ret = pl.exists()
    
    if(ret):
        print(file_path + " exist.")
    else:
        print(file_path + " do not exist.")
    
    if(pl.is_file()):
        print(file_path + " is a file.")
       
    if(pl.is_dir()):
        print(file_path + " is a directory.")
    
    return ret

# Check file/folder status by os.access method.
def checkFileStatusByOSAccess(file_path):
    # If this file exist.
    if(os.access(file_path, os.F_OK)):
        print(file_path + " exist.")
    else:
        print(file_path + " do not exist.")
            
    if(os.access(file_path, os.R_OK)):
        print(file_path + " is readable.")
        
    if(os.access(file_path, os.W_OK)):
        print(file_path + " is writable.")    
        
    if(os.access(file_path, os.EX_OK)):
        print(file_path + " is executable.")

# Create a new file and write some text in it.
def createNewFile(file_path):
    file_object = open(file_path, 'w')
    file_object.write('File is created.')
    print(file_path + " has been created. ")
    
# Create a new directory.
def createNewFolder(file_path):
    if(not checkFileExistByOSPath(file_path)):
        os.mkdir(file_path)
        print(file_path + " has been created. ")

# Change the file permission to read and execute only.
def setFilePermission(file_path):
    os.chmod(file_path, stat.S_IEXEC | stat.S_IREAD)
     
        
if __name__ == '__main__':
    file_folder = "./test"
    createNewFolder(file_folder)
    
    file_path = file_folder + "/abc.txt"
    # Check file existence.
    # fileExist = checkFileExistByException(file_path)
    # fileExist = checkFileExistByOSPath(file_path)
    fileExist = checkFileExistByPathlib(file_path)
    # If file do not exist then create it.
    if(not fileExist):
        createNewFile(file_path)
        setFilePermission(file_path)

    checkFileStatusByOSAccess(file_path)