# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: users.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0busers.proto\"P\n\x0cregisterUser\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x1c\n\x05reply\x18\x03 \x01(\x0b\x32\r.requestReply\"M\n\tloginUser\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x1c\n\x05reply\x18\x03 \x01(\x0b\x32\r.requestReply\"O\n\ndeleteUser\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x11\n\tfrom_user\x18\x02 \x01(\t\x12\x1c\n\x05reply\x18\x03 \x01(\x0b\x32\r.requestReply\")\n\tdumpUsers\x12\x1c\n\x05reply\x18\x01 \x01(\x0b\x32\r.requestReply\"=\n\x0b\x66ilterUsers\x12\x10\n\x08wildcard\x18\x01 \x01(\t\x12\x1c\n\x05reply\x18\x02 \x01(\x0b\x32\r.requestReply\"\x1d\n\x0crequestReply\x12\r\n\x05reply\x18\x01 \x01(\t2\xdf\x01\n\tUserTable\x12,\n\x0cRegisterUser\x12\r.registerUser\x1a\r.requestReply\x12&\n\tLoginUser\x12\n.loginUser\x1a\r.requestReply\x12(\n\nDeleteUser\x12\x0b.deleteUser\x1a\r.requestReply\x12&\n\tDumpUsers\x12\n.dumpUsers\x1a\r.requestReply\x12*\n\x0b\x46ilterUsers\x12\x0c.filterUsers\x1a\r.requestReplyb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'users_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REGISTERUSER._serialized_start=15
  _REGISTERUSER._serialized_end=95
  _LOGINUSER._serialized_start=97
  _LOGINUSER._serialized_end=174
  _DELETEUSER._serialized_start=176
  _DELETEUSER._serialized_end=255
  _DUMPUSERS._serialized_start=257
  _DUMPUSERS._serialized_end=298
  _FILTERUSERS._serialized_start=300
  _FILTERUSERS._serialized_end=361
  _REQUESTREPLY._serialized_start=363
  _REQUESTREPLY._serialized_end=392
  _USERTABLE._serialized_start=395
  _USERTABLE._serialized_end=618
# @@protoc_insertion_point(module_scope)