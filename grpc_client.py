# massive thanks: https://github.com/grpc/grpc/blob/master/examples/protos/helloworld.proto

from __future__ import print_function

import logging
import sys

import grpc
import users_pb2
import users_pb2_grpc

account = (-1, -1)

def run(server_addy, comm):
    elements = comm.split(' ')
    with grpc.insecure_channel(server_addy) as channel:
        stub = users_pb2_grpc.UserTableStub(channel)

        response = "no response"
        match elements[0]:
            case "register": #HOW TO CONSTRICT SIZE OF STRING
                response = stub.RegisterUser(users_pb2.registerUser(username=elements[1], password=elements[2]))
                print(response.reply)
            case "login":
                account = elements[1],elements[2]
                response = stub.LoginUser(users_pb2.loginUser(username=elements[1], password=elements[2]))
            case "deleteacc":
                response = stub.DeleteUser(users_pb2.deleteUser(username=elements[1], from_user = account[1], password=account[2]))
                    #reasoning: if a client can login to an account (ie has access to an account password), they can delete that account. else, cannot
            case "accdump":
                response = stub.DumpUsers(users_pb2.dumpUsers())
            case "accfilter":
                response = stub.FilterUsers(users_pb2.filterUsers(wildcard=elements[1]))
            case _:
                print("[FAILURE] Incorrect command usage.")
        print (response)


if __name__ == '__main__':
    logging.basicConfig()
    #ip = str(sys.argv[1]) #currently not using command line ip address (assuming localhost)
    #port = int(sys.argv[2]) #currently not using command line port
    comm = input() #add permanent listener, and server broadcast listener
    run('localhost:50051', comm)
