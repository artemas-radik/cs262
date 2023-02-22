import logging
import sys
sys.path.insert(1, '../')
sys.path.insert(1, '../test_cases/')
import grpc
import users_pb2
import users_pb2_grpc

import grpc_client

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

"""Integrated Tests (Robustness) -- commands_lst.txt"""
def robustness_tests(ip, port, verbose=False):
    client_start = grpc_client.Client(f'{ip}:{port}')

    fname = "../test_cases/commands_lst.txt"
    commands_list = construct_cl(fname, [])
    if (verbose): print(commands_list)

    for comm in commands_list:
        r = client_start.run(f'{ip}:{port}', comm, False)
        if (verbose):
            print(r)

if __name__ == "__main__":
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    verbose = False
    try:
        verbose = bool(sys.argv[3])
    except:
        pass
    robustness_tests(ip, port, verbose)
    print("Test suite passed.")