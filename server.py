import socket
import select
import sys
import re
from _thread import *

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
	print ("Correct usage: script, IP address, port number")
	exit()

# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])

# takes second argument from command prompt as port number
Port = int(sys.argv[2])

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

def clientthread(conn, addr, list_of_clients):

	# sends a message to the client whose user object is conn
	conn.send("Welcome to this chatroom!".encode('utf-8'))

	while True:
			try:
				message = conn.recv(2048).decode('utf-8')

				if message:
					print ("<" + addr[0] + "> " + message.strip())
					message_to_send = "<" + addr[0] + "> " + message
					broadcast(message_to_send, conn, list_of_clients)
				else:
					"""message may have no content if the connection
					is broken, in this case we remove the connection"""
					print("client conn broken")
					remove(conn, list_of_clients)

			except:
				continue

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection, list_of_clients):
	for client in list_of_clients:
		if client!=connection:
			try:
				client.send(message.encode('utf-8'))
			except:
				client.close()
				# if the link is broken, we remove the client
				remove(client)

"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection, list_of_clients):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

def err(client, message):
	client.send(struct.pack('B256s', 6, message.encode('ascii')))

def suc(client, message):
	qwdee = (7).to_bytes(1, 'big') + len(message).to_bytes(2, 'big') + message.encode('ascii')
	print(qwdee)
	client.send(qwdee)

def nms(client, from_username, content):
	client.send(struct.pack('B16s512s', 8, from_username.strip().encode('ascii'), content.strip().encode('ascii')))

if __name__ == "__main__":
	list_of_clients = []
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	IP_address = str(sys.argv[1])
	Port = int(sys.argv[2])
	server.bind((IP_address, Port))
	server.listen(100)

	while True:
		conn, addr = server.accept()
		list_of_clients.append(conn)
		print (addr[0] + " connected")
		start_new_thread(clientthread,(conn,addr, list_of_clients))	

	conn.close()
	server.close()