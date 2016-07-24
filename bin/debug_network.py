import socket
from struct import *
import numpy as np
from datetime import datetime


class UDP():
    def __init__(self, port = 12345):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.bind()

    def bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        print("udp : ", (self.host, self.port))

    def receive(self, skip = False):
        a = self.sock.recv(65535)
        print a

class TCP():
    def __init__(self, port = 12345):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.serversock = None
        self.clientsock = None
        self.bind()

    def bind(self):
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversock.bind((self.host, self.port))
        self.serversock.listen(10)
        print("<SettingValue>%s</SettingValue>\n<SettingValue>%d</SettingValue>" % (self.host, self.port))
        self.clientsock, client_address = self.serversock.accept()

    def receive(self, skip = False):
        a = self.clientsock.recv(65535)
        print a


import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('port', action='store', type=int, help='')
args = parser.parse_args()

receiver = TCP(port = args.port)
while 1:
    received = datetime.now()
    receiver.receive()
    print(( received - datetime.now()).microseconds)
