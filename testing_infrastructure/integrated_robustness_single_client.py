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
            

"""Single Client + Server: Automated Test -- commands_lst.txt"""

#commands to run:
    #python3 server.py ip 5000
    #python3 integrated_tests.py ip 5000
#note: must restart server upon each run

def integrated_robustness_single_client(ip, port, verbose=False):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #ip = str(sys.argv[1])
    #port = int(sys.argv[2])
    server.connect((ip, port))

    #randomized_commands(100, 8, 'commands_lst.txt') #run once

    commands_list = []
    fname = "../test_cases/commands_lst.txt"

    commands_list = construct_cl(fname, commands_list)
    if (verbose): print(commands_list)

    i = output = 0

    while i < len(commands_list):
        sockets_list = [sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:
            if socks == server:
                m = socks.recv(4096).decode('utf-8')
                if (verbose): print(m)
                #output = #just checking robustness, not server state!
                server.send(commands_list[i].encode('utf-8'))
                i += 1
            else:
                pass
    return True

if __name__ == "__main__":
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    integrated_robustness_single_client(ip, port, True)