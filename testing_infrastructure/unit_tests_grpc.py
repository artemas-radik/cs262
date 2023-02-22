import logging
import sys
sys.path.insert(1, '../')
sys.path.insert(1, '../test_cases/')
import grpc
import users_pb2
import users_pb2_grpc

import grpc_client


"""Single Client + Server: Account Tests -- m1_grpc.txt"""
def unit_tests(ip, port, verbose=False):
    client_start = grpc_client.Client(f'{ip}:{port}')
    f = open('../test_cases/m1_grpc.txt', 'r')
    f_out = open('../test_cases/m1_output_grpc.txt', 'r')

    comm = f.readline()
    o = f_out.readline()
    while comm:
        r = client_start.run(f'{ip}:{port}', comm.strip(), False)
        if (verbose):
            print(r)
        print(o.strip().find(r.strip()) != -1)
        comm = f.readline()
        o = f_out.readline()

if __name__ == "__main__":
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    verbose = False
    try:
        verbose = bool(sys.argv[3])
    except:
        pass
    unit_tests(ip, port, verbose)