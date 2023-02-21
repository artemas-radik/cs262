import sys
sys.path.insert(1, '../')
sys.path.insert(1, '../test_cases/')
import socket
import select
import unittest


"""Single Client + Server: Account Tests -- m1.txt"""
"""
#commands to run:
    #python3 server.py ip port
    #python3 server_unit_tests.py ip port
#note: must restart server upon each run

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((ip, port))

f = open('../test_cases/m1.txt', 'r')
f_out = open('../test_cases/m1_output.txt', 'r')

l = output = 1

while l:
    sockets_list = [sys.stdin, server]
    
    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            m = socks.recv(4096).decode('utf-8')
            print(m, m == output)
            output = f_out.readline().strip()
            l = f.readline().strip()
            server.send(l.encode('utf-8'))
        else:
            pass"""

"""Single Client + Server: Message Tests -- m2.txt"""
#commands to run:
    #python3 server.py ip port
    #python3 server_unit_tests.py ip port
#note: must restart server upon each run

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((ip, port))

f = open('../test_cases/m2.txt', 'r')
f_out = open('../test_cases/m2_output.txt', 'r')

l = output = 1

while l:
    sockets_list = [sys.stdin, server]
    
    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            m = socks.recv(4096).decode('utf-8')
            print(m, m == output)
            output = f_out.readline().strip()
            l = f.readline().strip()
            server.send(l.encode('utf-8'))
        else:
            pass


"""Single Client + Server: Random Tests -- commands_lst.txt """