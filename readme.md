# Getting Started
*Tested on MacOS Ventura 13.2 with Python 3.9.6 Installed*

Replace cases of `10.250.243.199` with your private IP address, obtained by running `ipconfig getifaddr en0` on wireless networks and `ipconfig getifaddr en1` on wired networks.

### Server
```bash
python3 server.py 10.250.243.199 5000
```

## Client
```bash
python3 client.py 10.250.243.199 5000
```

# Engineering Notebook
#### *February 7th, 2023*
We started the project today by following a guide for a similar project available [here](https://www.geeksforgeeks.org/simple-chat-room-using-python/) . Our goal for the moment is to acheive what the guide claims to acheive: a simple client-server chat program, where simple text messages can be sent to the server by clients and then rebroadcasted to every other client. Unfortunately the code provided by the guide does not work out-of-the-box and has the following issues:
1. Clients enter infinite loop state after server terminates. Server enters infinite loop state after client terminates.
2. Bytes not properly encoded/decoded to `utf-8` on both client and server side.
3. Multiple clients from the same IP address not served properly (dropped messages).

*We address Issue 1A by checking for the "server terminated" message (0 or an empty string) every time the client receives a message. Per advice [here](https://stackoverflow.com/questions/19795529/python-troubles-controlling-dead-sockets-through-select). Upon receiving the "server terminated" message, we terminate the client.*

## Wire Protocol

We use Python's `Lib/struct.py` to encode/decode messages efficiently and safely between our client and server. 

### Format Strings

> Format strings are the mechanism used to specify the expected layout when packing and unpacking data. They are built up from [Format Characters](https://docs.python.org/3.7/library/struct.html#format-characters), which specify the type of data being packed/unpacked.

**Note that all strings in this project are `ascii` encoded.** Thus, a string's size is equivalent to its length in all cases, as one `ascii` character takes one byte to store. Checks are in place client side to prevent usage of non-`ascii` strings.

### Transfer Buffer

The transfer buffer defines the structure of any and all messages exchanged between the client and server. We define the transfer buffer in this project as the union of a *Message Code* and a *Payload*. The first byte of any exchanged message is the *Message Code*, and the remaining bytes are the *Payload*. The *Message Code* has a Format Character of `B`, which maps to a C `unsigned char`. Each *Message Code* maps to a *Message Type*, which is an internal identifier introduced for accessibility and readibilty purposes. For instance, the client program labels its commands via the associated *Message Type* that they broadcast. Message codes `0...5` are requests made by a client to the server, and message codes `6...8` are responses made by the server to a client. Each message code is described in detail below. The *Payload Parameters* are combined sequentially in-order to form the *Payload*.

##### Requests 

Message Code: Type | Description | Payload Parameters
------------ | ------------ | ------------
0: `reg` | Register account. | username: `16s`, password :`64s`
1: `log` | Log in existing account. | username: `16s`, password: `64s`
2: `del` | Delete account. |
3: `acd` | Dump all account names. |
4: `acf` | Filter account names. | wildcard: `16s`
5: `msg` | Send a chat message to a user. | to_username: `16s`, content: `512s`

##### Responses

Message Code: Type | Description | Payload Parameters
------------ | ------------ | ------------ 
6: `err` | Error message. | message:`256s`
7: `suc` | Success message. | message:`256s`
8: `nms` | New chat message. | from_username:`16s`, content:`512s`


##### Testing Framework

General notes:
- justify the message codes we implemented (inclusion, exclusion of certain functionality)
- 


Spec:
server should never crash
- when server terminates, clients should terminate
client should never infinite loop
client should never return a result != truth on server


https://www.quora.com/How-do-I-test-a-distributed-system
Concurrency bugs
Inadequate failure handling
Incorrect input validation (usually leading to security bugs) or flawed threat models


https://web.stanford.edu/~engler/osdi2002.pdf
- not model checker


https://www.cs.cmu.edu/~aldrich/courses/17-355-18sp/notes/notes14-symbolic-execution.pdf
- symbolic execution isn't really testing our potential fail points


https://docs.python.org/3/library/unittest.html
- library providing testing framework

Server design:
- We want our server to be deterministic.

Testing design:
- repeatability

Command to generate gRPC code from users.proto
python3 -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. ./users.proto

Reference this post: https://groups.google.com/g/grpc-io/c/iLHgWC8o8UM/m/2PN4WaA9anMJ
- lazy auth
