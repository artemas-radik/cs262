import socket, select, sys

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        ip = str(sys.argv[1])
        port = int(sys.argv[2])
    except:
        ip = "52.152.216.212"
        port = 5000
    server.connect((ip, port))

    while True:
        sockets_list = [sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
        for socks in read_sockets:
            if socks == server:
                m = socks.recv(4096).decode("utf-8")
                if (m == ''):
                    break
                message = print(m)
            else:
                server.send(sys.stdin.readline().strip().encode('utf-8'))
