# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 08:24:55 2019

WITH CODE FROM: https://docs.python.org/3/library/socketserver.html

@author: Vishal Patel
"""

import socket

HOST, PORT = "localhost", 6464
test_data = [ "Test Data 0"
             ,"Test Data 1"
             ,'GET /SQL?=%22SELECT%20author%20FROM%20Stories%20WHERE%20author%20LIKE%20%27hellohello%%27%22 HTTP/1.1'
             ,'POST /URL?=https://www.fanfiction.net/s/12606073/39/ HTTP/1.1'
             ]

for data in test_data:
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))
    
        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
        sock.close()
    
    print("Sent:     {}".format(data))
    print("Received: {}".format(received))
    
print("DONE")