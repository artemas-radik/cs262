import socket
import select
import sys
from enum import Enum

class Payload(Enum):
    register = 0
    login = 1
    deleteacc = 2
    accdump = 3
    accfilter = 4
    message = 5
    error = 6
    success = 7
    newmessage = 8
 
def decode(buffer):
    match buffer[0]:
        case Payload.error.value:
            return f"[WARNING] {buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')}"
        case Payload.success.value:
            return f"[SUCCESS] {buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')}"
        case Payload.newmessage.value:
            return f"[MESSAGE] <{buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')}> {buffer[int.from_bytes(buffer[1:3],'big')+3:]}"
        case _:
            sys.exit(f"[FAILURE] Undecodable transfer buffer received.")

def encode(command):
    elements = command.split(' ')
    # TODO: Check fields to make sure they fit in types.
    match elements[0]:
        case Payload.register.name:
            return Payload.register.value.to_bytes(1, 'big') + len(elements[1]).to_bytes(2, 'big') + elements[1].encode('ascii') + len(elements[2]).to_bytes(2, 'big') + elements[2].encode('ascii')
        case Payload.login.name:
            return Payload.login.value.to_bytes(1, 'big') + len(elements[1]).to_bytes(2, 'big') + elements[1].encode('ascii') + len(elements[2]).to_bytes(2, 'big') + elements[2].encode('ascii')
        case Payload.deleteacc.name:
            return Payload.deleteacc.value.to_bytes(1, 'big')
        case Payload.accdump.name:
            return Payload.accdump.value.to_bytes(1, 'big')
        case Payload.accfilter.name:
            return Payload.accfilter.value.to_bytes(1, 'big') + len(elements[1]).to_bytes(2, 'big') + elements[1].encode('ascii')
        case Payload.message.name:
            return Payload.login.value.to_bytes(1, 'big') + len(elements[1]).to_bytes(2, 'big') + elements[1].encode('ascii') + len(elements[2]).to_bytes(2, 'big') + elements[2].encode('ascii')
        case _:
            print("[FAILURE] Incorrect command usage.")


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    server.connect((ip, port))

    while True:
        sockets_list = [sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:
            if socks == server:
                message = print(decode(socks.recv(4096)))
            else:
                server.send(encode(sys.stdin.readline().strip()))
