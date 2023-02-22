import logging
import sys
import time
sys.path.insert(1, '../')
sys.path.insert(1, '../test_cases/')
import grpc
import users_pb2
import users_pb2_grpc

import grpc_client

def paddle_tests(ip, port, verbose=False):
    client_start = grpc_client.Client(f'{ip}:{port}')
    client_start.run(f'{ip}:{port}', "register a b", False)
    client_start.run(f'{ip}:{port}', "login a b", False)
    n = 30
    t_end = time.time() + n
    i = 0
    while time.time() < t_end:
        #r = client_start.run(f'{ip}:{port}', "message a yo", False)
        client_start.run(f'{ip}:{port}', "message a 1", True)
        i += 1
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