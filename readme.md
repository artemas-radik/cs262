
# Client Quickstart
To make demo day convenient, we have precompiled our client for unix-based systems and defaulted it to connecting to a prehosted version of our server running on Azure cloud.
### Unix-Based Systems (MacOS, Linux)
Make sure you are in the root `cs262` directory. Run the precompiled binary with the following command:
```bash
./dist/client/client
```

### Windows
> Note that we have not tested on Windows, so support is experimental.

You can still use our prehosted server, but we have not precompiled a binary for you. You will have to run our client using Python `3.10` or `3.11`.
```bash
python3.10 client.py
```

## Usage
Let's say our username is `hello` and our password is `world`. After starting the client we would run `register hello world` to register our account, followed by `login hello world` to log ourselves in. Now that we are authenticated we are free to send and receive messages, retrieve account usernames, and delete our account. A full table of command functionality is included below.

Command & Parameters | Description 
------------ | ------------ 
`register [USR] [PWD]` | Register account. 
`login [USR] [PWD]` | Login existing account. 
`deleteacc` | Delete account. 
`accdump`| Dump all account names. 
`accfilter [WLDCRD]` | Filter account names. 
`message [USR] [MSG]` | Send a chat message to a user. 

# Manual Start
### Client
The client program takes two runtime parameters, an IP address and port. These parameters are hardcoded to default to `52.152.216.212` and `5000`, where we're hosting our server on Azure. Here is a sample usage of the client, to connect to our Azure server.
```bash
python3.10 client.py 52.152.216.212 5000
```
There is also our gRPC implementation of the client, which is started similarly.
> Note that we are not hosting an instance of the gRPC server.
```bash
python3.10 grpc_client.py 52.152.216.212 5001
```
### Server
The server program also takes two runtime parameters, an IP address and port. If you're on MacOS you can get your IP address by running `ipconfig getifaddr en0` on wireless networks and `ipconfig getifaddr en1` on wired networks. Here is a sample usage of the server, as we start it on our Azure server.
```bash
python3.10 server.py 52.152.216.212 5000
```
There is also our gRPC implementation of the server, which is started similarly.
```bash
python3.10 grpc_server.py 52.152.216.212 5001
```
### Tests
We have built test suites for 





# Engineering Notebook
#### *February 7th, 2023*
We started the project today by following a guide for a similar project available [here](https://www.geeksforgeeks.org/simple-chat-room-using-python/) . Our goal for the moment is to acheive what the guide claims to acheive: a simple client-server chat program, where simple text messages can be sent to the server by clients and then rebroadcasted to every other client. Unfortunately the code provided by the guide does not work out-of-the-box and has the following issues:
1. Clients enter infinite loop state after server terminates.
2. Bytes not properly encoded/decoded to `utf-8` on both client and server side.
3. Multiple clients from the same IP address not served properly (dropped messages).

*We address Issue 1 by checking for the "server terminated" message (0 or an empty string) every time the client receives a message. Per advice [here](https://stackoverflow.com/questions/19795529/python-troubles-controlling-dead-sockets-through-select). Upon receiving the "server terminated" message, we terminate the client.*

*We address Issue 2 by calling python encode('utf-8')/decode('utf-8') on all messages.*

## Wire Protocol

We use Python's `Lib/struct.py` to encode/decode messages efficiently and safely between our client and server. 

### Format Strings

> Format strings are the mechanism used to specify the expected layout when packing and unpacking data. They are built up from [Format Characters](https://docs.python.org/3.7/library/struct.html#format-characters), which specify the type of data being packed/unpacked.

**Note that all strings in this project are `ascii` encoded.** Thus, a string's size is equivalent to its length in all cases, as one `ascii` character takes one byte to store. Checks are in place client side to prevent usage of non-`ascii` strings.

### Transfer Buffer

The transfer buffer defines the structure of any and all messages exchanged between the client and server. We define the transfer buffer in this project as the union of a *Message Code* and a *Payload*. The first byte of any exchanged message is the *Message Code*, and the remaining bytes are the *Payload*. The *Message Code* has a Format Character of `B`, which maps to a C `unsigned char`. Each *Message Code* maps to a *Message Type*, which is an internal identifier introduced for accessibility and readibilty purposes. For instance, the client program labels its commands via the associated *Message Type* that they broadcast. Message codes `0...5` are requests made by a client to the server, and message codes `6...8` are responses made by the server to a client. Each message code is described in detail below. The *Payload Parameters* are combined sequentially in-order to form the *Payload*.

> **Arty: pls make edits to the wire protocol section as appropriate.** 

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

#### *February 17th, 2023*
### Design Spec

Design principles:
1. Robustness against user: the server should not crash as the result of a client command. 
2. Modularity: an account should not perform delete/logout actions on any other account.
3. Robustness against network: communication should be reasonably robust to network failure.

To uphold these principles, we:
1. Implement rigorous error handling.
2. Restrict logins:
	1. Only allow one login per client connection.
	2. Only allow one device logged in per account.
		1. Optimizing for simplicity and code cleanliness.
3. Queue messages to offline accounts.
	1. Note: we do not require confirmation of message receipt.

### Testing Infrastructure

We build unit tests following the principles outlined by [Nathan Peck](https://medium.com/@nathankpeck/microservice-testing-unit-tests-d795194fe14e), via Medium. The goal of unit testing is to isolate/test specific functionality in a single network component. We implement unit testing in server_unit_tests.py. The first test suite is for account management functionality. We compare expected results against generated results, for a manually designed set of commands. The second test suite is for simple message functionality (processing & error handling), again via a manually designed set of commands. 

We implement integrated testing in integrated_testing.py. The first test suite is for robustness against redundant or illogical commands. Runs a set of randomly generated commands from a single client. The second test suite is manually designed integrated testing, for all functionality over multiple clients. This is where most of the rigorous edge case testing takes place. The third test suite is once again for robustness, over a set of randomly generated commands, this time with multiple clients. 

A couple design goals we kept in mind: we want our server to be deterministic, and our testing to be repeatable. Background research which was especially helpful in informing our infrastructure decisions: [Don't Write Tests](https://www.youtube.com/watch?v=hXnS_Xjwk2Y), and [Testing a Distributed System](https://queue.acm.org/detail.cfm?id=2800697).

Test commands (wire protocol): 
start server: python3 server.py ip port v
- v = verbose flag, default = False
cd testing_infrastructure
python3 {test file name} ip port

Test commands (grpc): 
start server: python3 grpc_server.py ip port v
- v = verbose flag, default = False
cd testing_infrastructure
python3 {test file name} ip port

### Issues

Testing revealed the following issues:
1. Server allows multiple logins per client, returns a blank stare on deleteacc
2. Multiple clients can log into the same account, but second client login forces first client logout
3. No confirmation message sent on successful deleteacc
4. Messages dropped if account logs off, logs back on
5. Error statements for failed message delivery do not accurately descibe the error

*We address Issue 1 by disallowing multiple accounts per client. We address Issue 2 by disallowing multiple clients per account.*

*Issue 3 was an encoding error. Have fixed with .encode('utf-8')*

*Issues 4 and 5 fixed via implementation of a message queue, and more rigorous error handling.*

#### *February 19th, 2023*
### gRPC

Remote Procedure Calls are a [communication paradigm](https://web.eecs.umich.edu/~mosharaf/Readings/RPC.pdf) operating by sending functions, as opposed to wire protocols, which operate by sending information. We build out basic chat functionality in gRPC as well, following [this](https://melledijkstra.github.io/science/chatting-with-grpc-in-python) github guide, for the purpose of efficiency comparison with our wire protocol.

Command to generate gRPC code from users.proto:
python3 -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. ./users.proto

Key differences between wire protocol and gRPC implementation:

gRPC lends itself less naturally well to user authentication. In our system, we have an account automatically add a password to future requests, per discussion [here](https://groups.google.com/g/grpc-io/c/iLHgWC8o8UM/m/2PN4WaA9anMJ).

The system is robust against incorrect usage, but does not have specific error messages as in the wire protocol (ie, is less user friendly). This is a design choice based on the structure of gRPC; verifying that an error was caused specifically by a logged off client, for example, would require the server to manually track logged in/off clients. With more time, we would implement more of user friendliness.

#### *February 20th, 2023*
### Discussion

https://jbrandhorst.com/post/grpc-binary-blob-stream/
- default max message size = 4MB

Paddle Test:

Wire Protocol Paddle Test ("1"):
Messages Exchanged (30 seconds): 575269

gRPC Paddle Test ("1"):
Messages Exchanged (30 seconds): 1945

Wire Protocol Paddle Test ("1111111111111111111111111111111111111111111111111111111111111111"):
Messages Exchanged (30 seconds): 512541

gRPC Paddle Test ('1111111111111111111111111111111111111111111111111111111111111111'):
Messages Exchanged (30 seconds): 1756

grpc:
Messages Exchanged (30 seconds): 1258

1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111