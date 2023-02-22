import sys
sys.path.insert(1, '../')
sys.path.insert(1, '../test_cases/')
import socket
import select
#from client import encode, decode
#from client_unit_tests import randomized_commands

"""Utils"""
def construct_cl(fname, cl):
    f = open(fname, 'r')
    l = f.readline()
    while l:
        lst = l.split(' ')
        if (lst[0] in ['register', 'login'] and len(lst) == 3):
            cl.append(l)
        elif (lst[0] in ['accdump'] and len(lst) == 1):
            cl.append(l)
        elif (lst[0] in ['accfilter', 'deleteacc'] and len(lst) == 2):
            cl.append(l)
        l = f.readline()
    return cl

def randomized_commands(n, m, fname):
    letters = string.ascii_lowercase #thanks https://pynative.com/python-generate-random-string/
    letters += '.^$*+?\{\}[]\\|()'
    args = []

    for i in range(2):
        sub_str = ''.join(random.choice(letters) for j in range(m))
        args.append(sub_str)

    lst = [""]*n
    for i in range(n):
        x = int(random.random() * len(Payload))
        y = int(random.random() * len(Payload))
        s = Payload(x).name
        lst[i] = f"{s} {' '.join(sub_str+str(y) for sub_str in args)}"
    
    with open(fname, 'w') as fp: #thanks https://pynative.com/python-write-list-to-file/
        for comm in lst:
            fp.write("%s\n" % comm)


"""Multiple Clients + Server: Manual Test -- m3.txt"""
#commands to run:
    #python3 server.py ip port
    #python3 integrated_tests.py ip port (starts two clients)
#note: must restart server upon each run

def integrated_edge_tests(ip, port, verbose=False):
    num_cases = passed_cases = 0
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #ip = str(sys.argv[1])
    #port = int(sys.argv[2])
    server.connect((ip, port))

    server_conn2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn2.connect((ip, port))

    f = open('../test_cases/m3.txt', 'r')
    f_out = open('../test_cases/m3_output.txt', 'r')

    l = output = 1
    i = 0

    while l:
        sockets_list = [sys.stdin, server, server_conn2]
        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:
            if socks == server or socks == server_conn2:
                m = socks.recv(4096).decode('utf-8').replace('\n', ' ')
                if (verbose): 
                    print(m, m == output)

                if (i == 0): 
                    i += 1
                    continue
                num_cases += 1
                if (m == output): passed_cases += 1

                l = f.readline().strip()
                output = f_out.readline().strip()
                if (i % 2 == 0):
                    server.send(l.encode('utf-8'))
                else:
                    server_conn2.send(l.encode('utf-8'))
                i += 1
            else:
                pass
    return [num_cases, passed_cases]

if __name__ == "__main__":
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    integrated_edge_tests(ip, port, True)