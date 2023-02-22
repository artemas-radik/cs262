import sys
sys.path.insert(1, '../')
sys.path.insert(1, '../test_cases/')
import socket
import select
import unittest

"""Single Client + Server: Message Tests -- m2.txt"""
#commands to run:
    #python3 server.py ip port
    #python3 server_unit_tests.py ip port
#note: must restart server upon each run

def message_unit_tests(ip, port, verbose=False):
    num_cases = passed_cases = 0
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                if (verbose):
                    print(m, m == output)
                num_cases += 1
                if (m == output): passed_cases += 1
                output = f_out.readline().strip()
                l = f.readline().strip()
                server.send(l.encode('utf-8'))
            else:
                pass
    return [num_cases-1, passed_cases]

if __name__ == "__main__":
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    verbose = bool(sys.argv[3])
    message_unit_tests(ip, port, verbose)