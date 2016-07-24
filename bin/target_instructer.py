import argparse
import socket
import os

parser = argparse.ArgumentParser(description='')
parser.add_argument('--port', dest='port', action='store', type=int, default=12347, help='')
args = parser.parse_args()

host = socket.gethostbyname(socket.gethostname())
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, args.port))

print("<SettingValue>%s</SettingValue>\n<SettingValue>%d</SettingValue>" % (host, args.port))

while 1:
    a = sock.recv(65535)
    print(a)
    os.system("say next %s" % a)
