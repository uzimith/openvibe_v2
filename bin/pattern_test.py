import argparse
import socket

parser = argparse.ArgumentParser(description='')
parser.add_argument('--ip', dest='ip', action='store', type=str, default="192.168.2.2", help='')

parser.add_argument('--port', dest='port', action='store', type=int, default=12345, help='')
args = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while 1:
    command = raw_input()
    sock.sendto(str(int(command)), (args.ip, args.port))
