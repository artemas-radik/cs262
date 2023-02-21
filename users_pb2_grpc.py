# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import users_pb2 as users__pb2


class UserTableStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterUser = channel.unary_unary(
                '/UserTable/RegisterUser',
                request_serializer=users__pb2.registerUser.SerializeToString,
                response_deserializer=users__pb2.requestReply.FromString,
                )
        self.LoginUser = channel.unary_unary(
                '/UserTable/LoginUser',
                request_serializer=users__pb2.loginUser.SerializeToString,
                response_deserializer=users__pb2.requestReply.FromString,
                )
        self.DeleteUser = channel.unary_unary(
                '/UserTable/DeleteUser',
                request_serializer=users__pb2.deleteUser.SerializeToString,
                response_deserializer=users__pb2.requestReply.FromString,
                )
        self.DumpUsers = channel.unary_unary(
                '/UserTable/DumpUsers',
                request_serializer=users__pb2.dumpUsers.SerializeToString,
                response_deserializer=users__pb2.requestReply.FromString,
                )
        self.FilterUsers = channel.unary_unary(
                '/UserTable/FilterUsers',
                request_serializer=users__pb2.filterUsers.SerializeToString,
                response_deserializer=users__pb2.requestReply.FromString,
                )
        self.MessageUser = channel.unary_unary(
                '/UserTable/MessageUser',
                request_serializer=users__pb2.messageUser.SerializeToString,
                response_deserializer=users__pb2.requestReply.FromString,
                )


class UserTableServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoginUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DumpUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FilterUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MessageUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserTableServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterUser': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterUser,
                    request_deserializer=users__pb2.registerUser.FromString,
                    response_serializer=users__pb2.requestReply.SerializeToString,
            ),
            'LoginUser': grpc.unary_unary_rpc_method_handler(
                    servicer.LoginUser,
                    request_deserializer=users__pb2.loginUser.FromString,
                    response_serializer=users__pb2.requestReply.SerializeToString,
            ),
            'DeleteUser': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteUser,
                    request_deserializer=users__pb2.deleteUser.FromString,
                    response_serializer=users__pb2.requestReply.SerializeToString,
            ),
            'DumpUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.DumpUsers,
                    request_deserializer=users__pb2.dumpUsers.FromString,
                    response_serializer=users__pb2.requestReply.SerializeToString,
            ),
            'FilterUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.FilterUsers,
                    request_deserializer=users__pb2.filterUsers.FromString,
                    response_serializer=users__pb2.requestReply.SerializeToString,
            ),
            'MessageUser': grpc.unary_unary_rpc_method_handler(
                    servicer.MessageUser,
                    request_deserializer=users__pb2.messageUser.FromString,
                    response_serializer=users__pb2.requestReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'UserTable', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserTable(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserTable/RegisterUser',
            users__pb2.registerUser.SerializeToString,
            users__pb2.requestReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LoginUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserTable/LoginUser',
            users__pb2.loginUser.SerializeToString,
            users__pb2.requestReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserTable/DeleteUser',
            users__pb2.deleteUser.SerializeToString,
            users__pb2.requestReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DumpUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserTable/DumpUsers',
            users__pb2.dumpUsers.SerializeToString,
            users__pb2.requestReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FilterUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserTable/FilterUsers',
            users__pb2.filterUsers.SerializeToString,
            users__pb2.requestReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MessageUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserTable/MessageUser',
            users__pb2.messageUser.SerializeToString,
            users__pb2.requestReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
