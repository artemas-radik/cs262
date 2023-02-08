# Getting Started
*Tested on MacOS Ventura 13.2 with Python 3.9.6 Installed*
## Server
```bash
python3 server.py 10.250.243.199 5000
```

## Client
```bash
python3 client.py 10.250.243.199 5000
```

## Known Issues

1. Clients enter infinite loop state after server terminates.
2. Bytes not properly decoded to `utf-8` string client side in some cases.
3. Multiple clients from the same IP address not served properly (dropped messages).

# Engineering Notebook
###### *February 7th, 2023*
