import logging
import sys
import time
import string
import random
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
        letters = string.ascii_lowercase 
        x = int(random.random()*4096)
        sub_str = ''.join(random.choice(letters) for j in range(x))
        client_start.run(f'{ip}:{port}', f"message a {sub_str}", True)
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