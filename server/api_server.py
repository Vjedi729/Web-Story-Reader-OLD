# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 21:43:54 2019

WITH CODE FROM: https://docs.python.org/3/library/socketserver.html
WITH INFO FROM: https://www.afternerd.com/blog/python-http-server/
LINE 36 FROM:   https://brokenbad.com/address-reuse-in-pythons-socketserver/

@author: Vishal Patel
"""
#import http.server
import socketserver
import urllib
from ffnet_scraper import FFnet_Story
import parse_utils as p
import djangoApi as dj 

def api_function(string):
    for label in ["GET", "POST"]:
        x, c = p.strip_label(string, label, postprocess = lambda x: x.strip())
        if c:
            break
    if not c:
        return 'ERROR: Label should be "GET" or "POST"'

    for method in ["/SQL?=", "/URL?="]:
        y, c = p.strip_label(x, method, postprocess = lambda x: x.strip())
        if c:
            break
    if not c:
        return 'ERROR: Label should be "SQL" or "URL"'
    print(label, method, y)
    z = y.split()
    query = urllib.parse.unquote_plus(z[0])

    if method == "/SQL?=":
        if label == "GET":
            return dj.makeHttpResponse(
                    "200 OK",
                    "application/json; charset=UTF-8",
                    dj.runSelect(query)
                    )
        if label == "POST":
            return dj.makeHttpResponse(
                    "200 OK",
                    "application/json; charset=UTF-8",
                    dj.runQuery(query)
                    )
    if method == "/URL?=":
        story = FFnet_Story(query)
        if label == "GET":
            return dj.makeHttpResponse(
                    "200 OK",
                    "application/json; charset=UTF-8",
                    story.toJson()
                    )
        if label == "POST":
            return dj.makeHttpResponse(
                    "200 OK",
                    "application/json; charset=UTF-8",
                    dj.runQuery(story.toInsertQuery("FF_Stories"))
                    )
    return "UNKNOWN ERROR on:" + string    

class API_TCPHandler(socketserver.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.

    Attributes:
        self.rfile:             the file-like stream of data from the request
        self.request:           socket object that holds the request
        self.client_address:    the client address
        self.server:            the server instance (in case that's useful?)
    """

    def handle(self):
        print("Connection from", self.client_address, "(Type", str(type(self.client_address)) + ')')
        data = self.rfile.readline().strip()
        print('Recieved Text <<', data, '>>')

        # DO THINGS HERE
        toSend = bytes(api_function(data.decode("utf-8")), "utf-8")

        print('Sending <<', toSend, '>>')
        self.wfile.write(bytes(toSend))
        self.request.close()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True

    HOST, PORT = "localhost", 6464
    server = socketserver.TCPServer((HOST, PORT), API_TCPHandler)
    server.serve_forever()
    print("DONE")

run_server()
