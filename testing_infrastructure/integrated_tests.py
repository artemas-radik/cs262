import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../')
import socket
import select
#import client, server
from client import encode, decode

"""Single Client + Server: Manual Test -- m1.txt"""

#START UP CLIENT
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "10.250.244.35" #str(sys.argv[1])
port = 5000 #int(sys.argv[2])
server.connect((ip, port))

while True:
    sockets_list = [sys.stdin, server] #need to add a trigger, but otherwise it should work
    
    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            message = print(decode(socks.recv(4096)))
        else:
            server.send(encode(sys.stdin.readline().strip()))

"""Single Client + Server: Automated Test"""