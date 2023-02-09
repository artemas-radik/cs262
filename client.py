import socket
import select
import struct
import sys
from enum import Enum

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Payload(Enum):
    reg = 0
    log = 1
    dlt = 2
    acd = 3
    acf = 4
    msg = 5
    err = 6
    suc = 7
    nms = 8
 
def decode(buffer):
    code, payload = struct.unpack('B528s', buffer)
    match code:
        case Payload.err.value:
            message = struct.unpack('256s272x', payload)
            return f"{bcolors.WARNING}[WARNING]: {message[0].decode('ascii')}{bcolors.ENDC}"
        case Payload.suc.value:
            message = struct.unpack('256s272x', payload)
            return f"{bcolors.OKGREEN}[SUCCESS]: {message[0].decode('ascii')}{bcolors.ENDC}"
        case Payload.nms.value:
            from_username, content = struct.unpack('16s512s', payload)
            return f"[{from_username.decode('ascii')}] {content.decode('ascii')}"
        case _:
            sys.exit(f"{bcolors.FAIL}[FAILURE]: Undecodable transfer buffer received.{bcolors.ENDC}")

def encode(command):
    elements = command.split(' ')
    # TODO: Check fields to make sure they fit in types.
    match elements[0]:
        case Payload.reg.name:
            pass
        case Payload.log.name:
            pass
        case Payload.dlt.name:
            pass
        case Payload.acd.name:
            pass
        case Payload.acf.name:
            pass
        case Payload.msg.name:
            pass

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    sys.exit(f"{bcolors.FAIL}[FAILURE]: CORRECT USAGE: {bcolors.ENDC}{bcolors.BOLD}python3 client.py [IP] [PORT]{bcolors.ENDC}")
ip = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((ip, port))

while True:
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            message = print(decode(socks.recv(529)))
        else:
            server.send(sys.stdin.readline().strip().encode('ascii'))
