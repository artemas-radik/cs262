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

# Engineering Notebook *Work In Progress*
#### *February 7th, 2023*
We started the project today by following a guide for a similar project available [here](https://www.geeksforgeeks.org/simple-chat-room-using-python/) . Our goal for the moment is to acheive what the guide claims to acheive: a simple client-server chat program, where simple text messages can be sent to the server by clients and then rebroadcasted to every other client. Unfortunately the code provided by the guide does not work out-of-the-box and has the following issues:
1. Clients enter infinite loop state after server terminates. Server enters infinite loop state after client terminates.
2. Bytes not properly encoded/decoded to `utf-8` on both client and server side.
3. Multiple clients from the same IP address not served properly (dropped messages).

*We address Issue 1A by checking for the "server terminated" message (0 or an empty string) every time the client receives a message. Per advice [here](https://stackoverflow.com/questions/19795529/python-troubles-controlling-dead-sockets-through-select). Upon receiving the "server terminated" message, we terminate the client.*

## Wire Protocol


### Request Code Map
*These messages are sent exclusively from the client to the server.*

Message Code | Message Type | Payload Format
------------ | ------------ | ------------ 
0 | `reg` | `16s64s`
1 | `log` | `16s64s`
2 | `del` | 
3 | `acd` | 
4 | `acf` | `16s`
5 | `msg` | `16s512s`

### Response Code Map
*These messages are sent exclusively from the server to the client.*

Message Code | Message Type | Payload Format
------------ | ------------ | ------------ 
6 | `err` | `256s`
7 | `suc` | `256s`
8 | `nms` | `256s`

### Message Types

###### Type `reg`

Payload Element | Description
------------ | ------------
`16s` | Username
`64s` | Password

We use `reg` to indicate a client's intention to create an account on the server.

> Human beings face ever more complex and urgent problems, and their effectiveness in dealing with these problems is a matter that is critical to the stability and continued progress of society.

 [!note]  Lorem ipsum dolor sit amet

[!note] ddd
dd

> [!note] 
> For the `'s'` format character, the count is interpreted as the length of the bytes, not a repeat count like for the other format characters; for example, `'10s'` means a single 10-byte string, while `'10c'`means 10 characters. If a count is not given, it defaults to 1. For packing, the string is truncated or padded with null bytes as appropriate to make it fit. For unpacking, the resulting bytes object always has exactly the specified number of bytes. As a special case, `'0s'` means a single, empty string (while`'0c'` means 0 characters).