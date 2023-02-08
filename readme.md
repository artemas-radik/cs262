# Getting Started
*Tested on MacOS Ventura 13.2 with Python 3.9.6 Installed*

Replace cases of `10.250.243.199` with your private IP address, obtained by running `ipconfig getifaddr en0` on wireless networks and `ipconfig getifaddr en1` on wired networks.

### Server
```bash
python3 server.py 10.250.243.199 5000
```

### Client
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

> Format strings are the mechanism used to specify the expected layout when packing and unpacking data. They are built up from [Format Characters](https://docs.python.org/3.7/library/struct.html#format-characters), which specify the type of data being packed/unpacked.

**Note that all strings in this project are `ascii` encoded.** Thus, a string's size is equivalent to its length in all cases, as one `ascii` character takes one byte to store. Checks are in place client side to prevent usage of non-`ascii` strings.

### Transfer Buffer

The transfer buffer defines the structure of any and all messages exchanged between the client and server. We define the transfer buffer in this project as the union of a *Message Code* and a *Payload*. The first byte of any exchanged message is the *Message Code*, and the remaining bytes are the Payload. The *Message Code* has a Format Character of `B`, which maps to a C `unsigned char`. Each *Message Code* maps to a *Message Type*, which is an internal identifier introduced for accessibility and readibilty purposes. For instance, the client program labels it's commands via the associated *Message Type* that they broadcast. Message codes `0...5` are requests made by a client to the server, and message codes `6...8` are responses made by the server to a client. Each message code is described in detail below.

##### Requests 

Message Code | Message Type | Payload Format | Description
------------ | ------------ | ------------ | ------------ 
0 | `reg` | `16s64s` | Register with `16s` username & `64s` password.
1 | `log` | `16s64s` | Log in with a `16s` username & `64s` password.
2 | `del` | | Delete account.
3 | `acd` | | Dump all account names.
4 | `acf` | `16s` | Filter account names according to a `16s` wildcard.
5 | `msg` | `16s512s` | Send a `512s` message to a `16s` username.

##### Responses

Message Code | Message Type | Payload Format
------------ | ------------ | ------------ 
6 | `err` | `256s`
7 | `suc` | `256s`
8 | `nms` | `256s`
