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

 #h/red==One of Swati or Artemas, decide/set up how we'll hand code off to our project partners. Describe here. ==
 
 #h/red==One of Swati or Artemas, check project spec against what's currently in the engineering notebook. ==

#h/red ==Swati: go through and comment code.==

# Engineering Notebook
#### *February 7th, 2023*
We started the project today by following a guide for a similar project available [here](https://www.geeksforgeeks.org/simple-chat-room-using-python/) . Our goal for the moment is to acheive what the guide claims to acheive: a simple client-server chat program, where simple text messages can be sent to the server by clients and then rebroadcasted to every other client. Unfortunately the code provided by the guide does not work out-of-the-box and has the following issues:
1. Clients enter infinite loop state after server terminates.
2. Bytes not properly encoded/decoded to `utf-8` on both client and server side.
3. Multiple clients from the same IP address not served properly (dropped messages).

*We address Issue 1 by checking for the "server terminated" message (0 or an empty string) every time the client receives a message. Per advice [here](https://stackoverflow.com/questions/19795529/python-troubles-controlling-dead-sockets-through-select). Upon receiving the "server terminated" message, we terminate the client.*

*We address Issue 2 by calling python encode('utf-8')/decode('utf-8') on all messages.*

#h/red ==Artemas, I'm dumb, please detail how we/you addressed Issue 3.==

## Wire Protocol

We use Python's `Lib/struct.py` to encode/decode messages efficiently and safely between our client and server. 

### Format Strings

> Format strings are the mechanism used to specify the expected layout when packing and unpacking data. They are built up from [Format Characters](https://docs.python.org/3.7/library/struct.html#format-characters), which specify the type of data being packed/unpacked.

**Note that all strings in this project are `ascii` encoded.** Thus, a string's size is equivalent to its length in all cases, as one `ascii` character takes one byte to store. Checks are in place client side to prevent usage of non-`ascii` strings.

### Transfer Buffer

The transfer buffer defines the structure of any and all messages exchanged between the client and server. We define the transfer buffer in this project as the union of a *Message Code* and a *Payload*. The first byte of any exchanged message is the *Message Code*, and the remaining bytes are the *Payload*. The *Message Code* has a Format Character of `B`, which maps to a C `unsigned char`. Each *Message Code* maps to a *Message Type*, which is an internal identifier introduced for accessibility and readibilty purposes. For instance, the client program labels its commands via the associated *Message Type* that they broadcast. Message codes `0...5` are requests made by a client to the server, and message codes `6...8` are responses made by the server to a client. Each message code is described in detail below. The *Payload Parameters* are combined sequentially in-order to form the *Payload*.

#h/red ==Artemas, pls make edits to the wire protocol section as appropriate.==

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

### Test Infrastructure



### Issues

*Issue: Server allows multiple logins to different accounts from same client, but freaks tf out when deleteacc is subsequently called.*
*Issue: A second client login to same account --> forced logout of first client*
*Issue: deleteacc confirmation not sending*
*Issue: Messages do not queue when client is temporarily logged off* #h/red==Artemas, please weigh in if I dealt with this suboptimally==
*Issue: Error statements for failed message deliver do not accurately describe the failure*

#h/red==Still open: *Issue: Client does not disconnect when Server crashes.*==

#### *February 19th, 2023*

### RPC

#### *February 20th, 2023*

### Results

