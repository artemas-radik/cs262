
# Quickstart
To make demo day convenient, we have provided three Microsoft Azure servers which are running our server code. These servers are geographically distributed across the following regions:
- US East
- US West
- Central Canada

Quickstarting the client utilizes these servers automatically. Quickstart the client by running
```bash
python3.10 client.py
```

### Engineering Notebook
Read our engineering notebook [here](https://github.com/artemas-radik/cs262/blob/main/latex/template.pdf).

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

# Server Start

### Server
The server program takes two runtime parameters, an IP address and port. If you're on MacOS you can get your IP address by running `ipconfig getifaddr en0` on wireless networks and `ipconfig getifaddr en1` on wired networks. Here is a sample usage of the server, as we start it on our Azure server.
```bash
python3.10 server.py 52.152.216.212 5000
```

### Unit Tests
We have built test files for several test cases. To run the tests, run our testing scri
```bash
./testing.bash
```

### Integration Tests
The integration tests can be performed manually. We have designed two tests. The first test is for two-fault tolerance:
1. Quickstart one client and run `regster a b` + `login a b`.
2. Quickstart another client and run `regster c d` + `login c d`.
3. Send a message from the first client via `message c hello`.
4. Kill two servers via the SSH key in our repository.
5. Repeat step three and see that the system remains operational.

The second test is for persistence:
1. After performing the above test, kill client `a`.
2. Try to send a message to `a`.
3. Reboot the last remaining server.
4. Log `a` back in and see that persistence is demonstrated.


# Wire Protocol
The wire protocol follows very closely to the table in the "Usage" seciton above. We use a string based transfer buffer. The first part of the transfer buffer is the command (opcode). For instance, `message` or `deleteacc`. If any parameters are necessary for a given command, we append them to transfer buffer, and ensure that all components of the transfer buffer are seperated by spaces. The only command that allows for a parameter to include spaces is `message`. For `message`, anything after the first parameter gets interpreted as part of the second parameter, so the second parameter is allowed to have spaces (message contents). All strings are `utf-8` encoded. The maximum allowed transfer buffer size is 4096 bytes.