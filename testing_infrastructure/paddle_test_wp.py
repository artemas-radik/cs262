import logging
import sys
import time
import socket
import select
sys.path.insert(1, '../')
sys.path.insert(1, '../test_cases/')

def paddle_tests(ip, port, verbose=False):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    server.send("register a b".encode('utf-8'))

    n = 30
    t_end = time.time() + n
    i = 0
    while time.time() < t_end:
        sockets_list = [sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:
            if socks == server:
                m = socks.recv(4096).decode('utf-8')
                print(m)
                if (i == 1):
                    server.send("login a b".encode('utf-8'))
                elif (i > 1):
                    server.send("message a 1".encode('utf-8'))
                i += 1
            else:
                pass
    print(f"Messages Exchanged ({n} seconds): {i}")

if __name__ == "__main__":
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    verbose = False
    try:
        verbose = bool(sys.argv[3])
    except:
        pass
    paddle_tests(ip, port, verbose)