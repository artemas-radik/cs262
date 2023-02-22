# massive thanks: https://github.com/grpc/grpc/blob/master/examples/protos/helloworld.proto

from __future__ import print_function

import logging
import sys
import threading

import grpc
import users_pb2
import users_pb2_grpc

class Client:

    #initialize class Client with local state variables
    def __init__(self, server_addy):
        self.account = [-1, -1]
        self.channel = grpc.insecure_channel(server_addy)
        self.stub = users_pb2_grpc.UserTableStub(self.channel)
        self.chat_list = []
        self.debug_fname = "debug_log.txt"
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

    def run(self, server_addy, comm, v=True):
        elements = comm.split(' ')

        response = 0
        match elements[0]:
            #usage: register a b
            case "register":
                response = self.stub.RegisterUser(users_pb2.registerUser(username=elements[1], password=elements[2]))
            #usage: login a b
            case "login":
                response = self.stub.LoginUser(users_pb2.loginUser(username=elements[1], password=elements[2]))
                if (response.reply.find("Auth") != -1):
                    self.account[0] = elements[1]
                    self.account[1] = elements[2]
            #usage: deleteacc
            case "deleteacc":
                try:
                    response = self.stub.DeleteUser(users_pb2.deleteUser(username=self.account[0], from_user = self.account[0], password=self.account[1]))
                    if (response.reply.find("Del") != -1):
                        self.account[0] = -1
                        self.account[1] = -1
                except:
                    pass
            #usage: accdump
            case "accdump":
                response = self.stub.DumpUsers(users_pb2.dumpUsers())
                #usage: accfilter
            case "accfilter":
                response = self.stub.FilterUsers(users_pb2.filterUsers(wildcard=elements[1]))
            #usage: message
            case "message":
                if self.account[0] != -1:
                    o = users_pb2.messageUser(username=elements[1], from_user = self.account[0], m = ' '.join(elements[2:]))
                    f = open(self.debug_fname, "a")
                    f.write(f"{sys.getsizeof(o)}\n")
                    response = self.stub.MessageUser(o)
            case _:
                pass
        if response != 0:
            response = response.reply
        else:
            response = "[FAILURE] Incorrect command usage."
        if v:
            print(response)
        else:
            return(response)

    #listen for messages from server
        #continuously running SubscribeMessages()
    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for note in self.stub.SubscribeMessages(users_pb2.requestReply()):  # this line will wait for new messages from the server!
            if (note.username == self.account[0]):
                print("<{}> {}".format(note.from_user, note.m))


if __name__ == '__main__':
    logging.basicConfig()
    try:
        ip = str(sys.argv[1]) #asssume ip = 'Localhost' for now
        port = int(sys.argv[2])
    except:
        ip = "52.152.216.212"
        port = "5001"
    #instantiate Client Object
    client_start = Client(f'{ip}:{port}')

    #infinite loop, wait for input commands
    while True:
        comm = input()
        client_start.run(f'{ip}:{port}', comm)
