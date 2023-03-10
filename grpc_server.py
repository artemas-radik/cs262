#massive thanks: https://github.com/grpc/grpc/blob/master/examples/protos/helloworld.proto

from concurrent import futures
import sys
import logging
import re

import grpc
import users_pb2
import users_pb2_grpc

accounts = {}

class UserTable(users_pb2_grpc.UserTableServicer):
    def __init__(self):
        # List with all the chat history
        self.chats = []

    #add key, value pair (username, password) to accounts
        #throw error if the username is already in accounts
            #prevents change of password
    def RegisterUser(self, request, context):
        if request.username in accounts.keys():
            return users_pb2.requestReply(reply="Username already registered.")
        accounts[request.username] = request.password
        return users_pb2.requestReply(reply= f"Registered {request.username}.")

    #authenticates login request
        #request.password must match stored password on server
    #load full chat history of user, upon login
        #similar to how FB messenger functions, for example
    def LoginUser(self, request, context):
        if request.username in accounts.keys():
            if accounts[request.username] == request.password:
                #accounts[request.username][1] = 1
                mess = [i for i,c in enumerate(self.chats) if c.username==request.username] #loads full chat history
                dump = '\n'.join([self.chats[i].m for i in mess])
                return users_pb2.requestReply(reply= f"Authenticated {request.username}. \n{dump}")
            else: 
                return users_pb2.requestReply(reply= f"Wrong password or username.") #can be triggered by both an incorrect password and incorrect username
        else:
            return users_pb2.requestReply(reply= f"Username not found.")

    #deletes user
        #removes account with username == request.username from accounts
        #checks password attached to client request
            #ensures a client can only delete its own account
    def DeleteUser(self, request, context):
        if request.username in accounts.keys():
            if request.username == request.from_user and accounts[request.username] == request.password:
                #simple auth
                del accounts[request.username]
                return users_pb2.requestReply(reply= f"Account Deleted.")
            else:
                return users_pb2.requestReply(reply= f"Not authenticated.")
        else:
            return users_pb2.requestReply(reply= f"User not found.")
        
    #return all registered users
        #iterates through accounts
        #DeleteUser already handles removal of usernames from accounts
    def DumpUsers(self, request, context):
        if accounts:
            dump = "Users: "
            for uname in accounts:
                dump += f" {uname},"
            return users_pb2.requestReply(reply= f"{dump[:-1]}.")
        else:
            return users_pb2.requestReply(reply= f"No users found.")

    #return all registered users, w/ matching regex
        #iterates through accounts
        #DeleteUser already handles removal of usernames from accounts
    def FilterUsers(self, request, context):
        if accounts:
            r = re.compile(request.wildcard)
            filtered_accs = list(filter(r.match, accounts)) #thanks https://stackoverflow.com/questions/3640359/regular-expressions-search-in-list
            if not len(filtered_accs):
                return users_pb2.requestReply(reply= f"No matching accounts.")
            else:
                dump = f"Matching Users: {', '.join(str(s) for s in filtered_accs)}." #thanks https://www.reddit.com/r/learnpython/comments/l10k8h/is_there_a_way_to_unpack_a_list_with_f_stings/ 
                return users_pb2.requestReply(reply= f"{dump}")
        else: 
            return users_pb2.requestReply(reply= f"No accounts found.")
    
    #appends messages to self.chats (triggers action by SubscribeMessages)
    def MessageUser(self, request, context):
        #logged_in = False
        #uname = "Guest"
        if request.username not in accounts:
            return users_pb2.requestReply(reply="User dne.") 
        self.chats.append(request)
        return users_pb2.requestReply()
    
    #yields every message added to chats
    def SubscribeMessages(self, request_iterator, context):
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                s = self.chats[lastindex]
                lastindex += 1
                yield s

def serve(ip, port):
    #port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UserTableServicer_to_server(UserTable(), server)
    #server.add_insecure_port('[::]:' + port)
    server.add_insecure_port(ip +':'+port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

#initialize server
if __name__ == '__main__':
    logging.basicConfig()
    try: 
        ip = str(sys.argv[1])
        port = str(sys.argv[2])
    except:
        ip = "52.152.216.212"
        port = "5001"
    serve(ip, port)
