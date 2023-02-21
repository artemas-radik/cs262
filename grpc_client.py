# massive thanks: https://github.com/grpc/grpc/blob/master/examples/protos/helloworld.proto

from __future__ import print_function

import logging
import sys

import grpc
import users_pb2
import users_pb2_grpc

class Client:

    def __init__(self):
        account = (-1, -1)
        #threading.Thread(target=self.__listen_for_messages, daemon=True).start()

    def run(self, server_addy, comm):
        elements = comm.split(' ')
        with grpc.insecure_channel(server_addy) as channel:
            stub = users_pb2_grpc.UserTableStub(channel) #is this conn?

            response = "no response"
            match elements[0]:
                case "register": #HOW TO CONSTRICT SIZE OF STRING
                    response = stub.RegisterUser(users_pb2.registerUser(username=elements[1], password=elements[2]))
                    print(response.reply)
                case "login":
                    self.account = elements[1], elements[2]
                    response = stub.LoginUser(users_pb2.loginUser(username=elements[1], password=elements[2]))
                case "deleteacc":
                    response = stub.DeleteUser(users_pb2.deleteUser(username=elements[1], from_user = self.account[0], password=self.account[1]))
                        #reasoning: if a client can login to an account (ie has access to an account password), they can delete that account. else, cannot
                case "accdump":
                    response = stub.DumpUsers(users_pb2.dumpUsers())
                case "accfilter":
                    response = stub.FilterUsers(users_pb2.filterUsers(wildcard=elements[1]))
                case "message":
                    response = stub.MessageUser(users_pb2.messageUser(username=elements[1], from_user = account[1], m = elements[2]))
                case _:
                    print("[FAILURE] Incorrect command usage.")
            print (response)

    def __listen_for_messages(self): #update conn input here
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for note in self.conn.ChatStream(chat.Empty()):  # this line will wait for new messages from the server!
            print("R[{}] {}".format(note.name, note.message))  # debugging statement
            self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))  # add the message to the UI


if __name__ == '__main__':
    logging.basicConfig()
    ip = str(sys.argv[1]) #asssume ip = 'Localhost' for now
    port = int(sys.argv[2])
    client_start = Client()

    while True:
        comm = input()
        client_start.run(f'{ip}:{port}', comm)
