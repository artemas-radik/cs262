#CREDITS PROF JAMES WALDO
import accountbook_pb2 as accountbook__pb2 #generate from accountbook.proto?

#why two underscores? ie why accountbook__pb2?

class AccountBookStub(object):

    def __init__(self, channel):

        self.CreateAccount = channel.unary_unary('/accountbook.AccountBook/CreateAccount', request_serializer=accountbook__pb2.Account.SerializetoString, response_deserializer = accountbook__pb2.requestReply.FromString,)

        self.GetAccountBalance = channel.unary_unary(
            '/accountbook.AccountBook/GetAccountBalance',
            request_serializer=accountbook__pb2.AccountId.SerializeToString,
            response_deserializer=accountbook__pb2.AccountBalance.FromString,
        )

        self.GetAccountOutstanding = channel.unary_unary(
            '/accountbook.AccountBook/GetAccountName',
            request_serialaizer = accountbook__pb2.AccountId.SerializeToString,
            response_deserializer=accountbook__pb2.AccountOutstanding.FromString,
        )

        self.GetAccountName = channel.unary_unary(
            '/accountbook.AccountBook/GetAccountName',
            request_serialaizer = accountbook__pb2.AccountId.SerializeToString,
            response_deserializer=accountbook__pb2.AccountName.FromString,
        )

        self.MakeDeposit = channel.unary_unary(
            '/accountbook.AccountBook/MakeDeposit',
            request_serialaizer = accountbook__pb2.makeDeposit.SerializeToString,
            response_deserializer=accountbook__pb2.requestReply.FromString,
        )

        self.MakeWithdrawal = channel.unary_unary(
            '/accountbook.AccountBook/MakeWithdrawal',
            request_serialaizer = accountbook__pb2.makeWithdrawal.SerializeToString,
            response_deserializer=accountbook__pb2.requestReply.FromString,
        )

        self.MakeTransfer = channel.unary_unary(
            '/accountbook.AccountBook/MakeTransfer',
            request_serialaizer = accountbook__pb2.makeTrasnfer.SerializeToString,
            response_deserializer=accountbook__pb2.requestReply.FromString,
        )

class AccountBookServicer(object):

    def CreateAccount(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountBalance(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountOutstanding(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLMENTED)
        context.set_details('Method not implemented')
        raise NotImplementedError('Method not implemented!')

    def GetAccountName(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MakeDeposit(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')