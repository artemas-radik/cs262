# Getting Started
*Tested on MacOS Ventura 13.2 with Python 3.9.6 Installed*

Replace cases of `10.250.243.199` with your private IP address, obtained by running `ipconfig getifaddr en0` on wireless networks and `ipconfig getifaddr en1` on wired networks.

## Server
```bash
python3 server.py 10.250.243.199 5000
```

## Client
```bash
python3 client.py 10.250.243.199 5000
```

# Engineering Notebook
#### *February 7th, 2023*
We started the project today by following a guide for a similar project available at https://www.geeksforgeeks.org/simple-chat-room-using-python/. Our goal for the moment is to acheive what the guide claims to acheive: a simple client-server chat program, where simple text messages can be sent to the server by clients and then rebroadcasted to every other client. Unfortunately the code provided by the guide does not work out-of-the-box has the following issues:
1. Clients enter infinite loop state after server terminates.
	1. Server enters infinite loop state after client terminates
2. Bytes not properly encoded/decoded to `utf-8` on both client and server side.
3. Multiple clients from the same IP address not served properly (dropped messages).
We address Issue 1A by checking for the "server terminated" message (0 or an empty string) every time the client receives a message. Per advice at: https://stackoverflow.com/questions/19795529/python-troubles-controlling-dead-sockets-through-select. Upon receiving the "server terminated" message, we terminate the client. 