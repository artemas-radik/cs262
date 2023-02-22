# massive thanks: https://github.com/grpc/grpc/blob/master/examples/protos/helloworld.proto

from __future__ import print_function

import logging
import sys
import threading

import grpc
import users_pb2
import users_pb2_grpc

class Client:

    def __init__(self, server_addy):
        self.account = [-1, -1]
        self.channel = grpc.insecure_channel(server_addy)
        self.stub = users_pb2_grpc.UserTableStub(self.channel)
        self.chat_list = []
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

    def run(self, server_addy, comm):
        elements = comm.split(' ')

        response = "[FAILURE] Incorrect command usage."
        match elements[0]:
            case "register":
                response = self.stub.RegisterUser(users_pb2.registerUser(username=elements[1], password=elements[2]))
            case "login":
                self.account = elements[1], elements[2]
                response = self.stub.LoginUser(users_pb2.loginUser(username=elements[1], password=elements[2]))
            case "deleteacc":
                response = self.stub.DeleteUser(users_pb2.deleteUser(username=elements[1], from_user = self.account[0], password=self.account[1]))
            case "accdump":
                response = self.stub.DumpUsers(users_pb2.dumpUsers())
            case "accfilter":
                response = self.stub.FilterUsers(users_pb2.filterUsers(wildcard=elements[1]))
            case "message":
                if self.account[0] != -1:
                    response = self.stub.MessageUser(users_pb2.messageUser(username=elements[1], from_user = self.account[0], m = ' '.join(elements[2:])))
            case _:
                print("[FAILURE] Incorrect command usage.")
        print(response.reply)

    def __listen_for_messages(self): #update conn input here
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for note in self.stub.SubscribeMessages(users_pb2.requestReply()):  # this line will wait for new messages from the server!
            if (note.username == self.account[0]):
                print("<{}> {}".format(note.from_user, note.m))


if __name__ == '__main__':
    logging.basicConfig()
    ip = str(sys.argv[1]) #asssume ip = 'Localhost' for now
    port = int(sys.argv[2])
    client_start = Client(f'{ip}:{port}')

    while True:
        comm = input()
        client_start.run(f'{ip}:{port}', comm)
