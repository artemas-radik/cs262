import logging
import sys
sys.path.insert(1, '../')
sys.path.insert(1, '../test_cases/')
import grpc
import users_pb2
import users_pb2_grpc

import grpc_client

"""Integrated Tests (Messaging) -- m3_grpc.txt """
def messaging_tests(ip, port, verbose=False):
    client1 = grpc_client.Client(f'{ip}:{port}')
    client2 = grpc_client.Client(f'{ip}:{port}')
    f = open('../test_cases/m3_grpc.txt', 'r')
    f_out = open('../test_cases/m3_output_grpc.txt', 'r')

    comm = f.readline()
    o = f_out.readline()
    i = 0
    while comm:
        if i % 2 == 0:
            r = client1.run(f'{ip}:{port}', comm.strip(), False)
        else:
            r = client2.run(f'{ip}:{port}', comm.strip(), False)
        if (verbose):
            print(r)
        print(o.strip().find(' '.join(r.strip().split("\n"))) != -1)
        comm = f.readline()
        o = f_out.readline()
        i += 1

if __name__ == "__main__":
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    verbose = False
    try:
        verbose = bool(sys.argv[3])
    except:
        pass
    messaging_tests(ip, port, verbose)