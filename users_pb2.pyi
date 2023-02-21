from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class deleteUser(_message.Message):
    __slots__ = ["from_user", "reply", "username"]
    FROM_USER_FIELD_NUMBER: _ClassVar[int]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    from_user: str
    reply: requestReply
    username: str
    def __init__(self, username: _Optional[str] = ..., from_user: _Optional[str] = ..., reply: _Optional[_Union[requestReply, _Mapping]] = ...) -> None: ...

class dumpUsers(_message.Message):
    __slots__ = ["reply"]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    reply: requestReply
    def __init__(self, reply: _Optional[_Union[requestReply, _Mapping]] = ...) -> None: ...

class filterUsers(_message.Message):
    __slots__ = ["reply", "wildcard"]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    WILDCARD_FIELD_NUMBER: _ClassVar[int]
    reply: requestReply
    wildcard: str
    def __init__(self, wildcard: _Optional[str] = ..., reply: _Optional[_Union[requestReply, _Mapping]] = ...) -> None: ...

class loginUser(_message.Message):
    __slots__ = ["password", "reply", "username"]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    password: str
    reply: requestReply
    username: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., reply: _Optional[_Union[requestReply, _Mapping]] = ...) -> None: ...

class messageUser(_message.Message):
    __slots__ = ["from_user", "m", "reply", "username"]
    FROM_USER_FIELD_NUMBER: _ClassVar[int]
    M_FIELD_NUMBER: _ClassVar[int]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    from_user: str
    m: str
    reply: requestReply
    username: str
    def __init__(self, username: _Optional[str] = ..., from_user: _Optional[str] = ..., m: _Optional[str] = ..., reply: _Optional[_Union[requestReply, _Mapping]] = ...) -> None: ...

class registerUser(_message.Message):
    __slots__ = ["password", "reply", "username"]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    password: str
    reply: requestReply
    username: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., reply: _Optional[_Union[requestReply, _Mapping]] = ...) -> None: ...

class requestReply(_message.Message):
    __slots__ = ["reply"]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    reply: str
    def __init__(self, reply: _Optional[str] = ...) -> None: ...
