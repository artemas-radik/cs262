#massive thanks: https://github.com/grpc/grpc/blob/master/examples/protos/helloworld.proto

from concurrent import futures
import logging
import re

import grpc
import users_pb2
import users_pb2_grpc

accounts = {}
    
#transmute payload success or payload error functionality!!

class UserTable(users_pb2_grpc.UserTableServicer):
    #return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    def RegisterUser(self, request, context):
        if request.username in accounts.keys():
            return users_pb2.requestReply(reply="Username already registered.")
        accounts[request.username] = request.password
        return users_pb2.requestReply(reply= f"Registered {request.username}.")

    def LoginUser(self, request, context):
        if request.username in accounts.keys():
            if accounts[request.username] == request.password:
                return users_pb2.requestReply(reply= f"Authenticated {request.username}.")
            else: 
                return users_pb2.requestReply(reply= f"Wrong password.")
        else:
            return users_pb2.requestReply(reply= f"Username not found.")

    def DeleteUser(self, request, context): #have not tested delete yet
        if request.username in accounts.keys():
            if request.username == request.from_user and accounts[request.username] == request.password:
                #simple auth
                del accounts[request.username]
                return users_pb2.requestReply(reply= f"Account Deleted.")
            else:
                return users_pb2.requestReply(reply= f"Not authenticated.")
        else:
            return users_pb2.requestReply(reply= f"User not found.")
        
    def DumpUsers(self, request, context):
        if accounts:
            dump = "Users: "
            for uname in accounts:
                dump += f"{uname}, "
            return users_pb2.requestReply(reply= f"{dump[:-2]}.")
        else:
            return users_pb2.requestReply(reply= f"No users found.")

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
    

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UserTableServicer_to_server(UserTable(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
