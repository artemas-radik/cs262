# Python program to implement server side of chat room.
import socket
import select
import re
import sys
'''Replace "thread" with "_thread" for python 3'''
from _thread import *
from enum import Enum

accounts = {}

class Payload(Enum):
    register = 0
    login = 1
    deleteacc = 2
    accdump = 3
    accfilter = 4
    message = 5
    error = 6
    success = 7
    newmessage = 8

class Account:
	def __init__(self, password):
		self.password = password

	def message(self, sender, content):
		self.socket.send(Payload.register.value.to_bytes(1, 'big') + len(sender).to_bytes(2, 'big') + sender.encode('ascii') + len(content).to_bytes(2, 'big') + content.encode('ascii'))

def encode(response, message):
    return response.value.to_bytes(1, 'big') + len(message).to_bytes(2, 'big') + message.encode('ascii')

def decode(buffer, socket):
	match buffer[0]:
		case Payload.register.value:
			username = buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')
			password = buffer[int.from_bytes(buffer[1:3],'big')+3:].decode('ascii')
			if username in accounts.keys():
				socket.send(encode(Payload.error, "Username already registered."))
				return
			accounts[username] = Account(password)
			socket.send(encode(Payload.success, f"Registered {username}."))

		case Payload.login.value:
			username = buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')
			password = buffer[int.from_bytes(buffer[1:3],'big')+3:].decode('ascii')
			if username in accounts.keys():
				if accounts[username].password == password:
					accounts[username].socket = socket
					socket.send(encode(Payload.success, f"Authenticated {username}."))
					return
				else:
					socket.send(encode(Payload.error, f"Wrong password."))
			socket.send(encode(Payload.error, f"Username not found."))

		case Payload.deleteacc.value:
			for account in accounts.keys():
				if accounts[account].socket == socket:
					del accounts[account]
					socket.send(encode(Payload.success, f"Account deleted."))
					return
			socket.send(encode(Payload.error, f"Not authenticated."))

		case Payload.accdump.value:
			if accounts:
				dump = "Users: "
				for account in accounts:
					dump += f"{account}, "
				socket.send(encode(Payload.success, dump[:-2]+"."))
				return
			else:
				socket.send(encode(Payload.error, "No accounts found."))
				return

		case Payload.accfilter.value:
			wildcard = buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii') #why extra processing?
			if accounts:
				r = re.compile(wildcard)
				filtered_accs = list(filter(r.match, accounts)) #thanks https://stackoverflow.com/questions/3640359/regular-expressions-search-in-list
				if not len(filtered_accs):
					socket.send(encode(Payload.success, "No matching accounts."))
				else:
					dump = f"Matching Users: {', '.join(str(s) for s in filtered_accs)}." #thanks https://www.reddit.com/r/learnpython/comments/l10k8h/is_there_a_way_to_unpack_a_list_with_f_stings/ 
					socket.send(encode(Payload.success, dump))
				return
			else:
				socket.send(encode(Payload.error, "No accounts found."))
				return

		case Payload.message.value:
			to = username = buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')
			content = buffer[int.from_bytes(buffer[1:3],'big')+3:].decode('ascii')
		case _:
			print("[FAILURE] Incorrect command usage.")

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

list_of_clients = []

def clientthread(conn, addr):

	# sends a message to the client whose user object is conn
	conn.send(bytes("Welcome to this chatroom!", 'utf-8'))

	while True:
			try:
				message = conn.recv(2048)
				if message:

					"""prints the message and address of the
					user who just sent the message on the server
					terminal"""
					print ("<" + addr[0] + "> " + message)

					# Calls broadcast function to send message to all
					message_to_send = "<" + addr[0] + "> " + message
					broadcast(message_to_send, conn)

				else:
					"""message may have no content if the connection
					is broken, in this case we remove the connection"""
					remove(conn)

			except:
				continue

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(bytes(message, "utf-8"))
			except:
				clients.close()

				# if the link is broken, we remove the client
				remove(clients)

"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:

	"""Accepts a connection request and stores two parameters,
	conn which is a socket object for that user, and addr
	which contains the IP address of the client that just
	connected"""
	conn, addr = server.accept()

	"""Maintains a list of clients for ease of broadcasting
	a message to all available people in the chatroom"""
	list_of_clients.append(conn)

	# prints the address of the user that just connected
	print (addr[0] + " connected")

	# creates and individual thread for every user
	# that connects
	start_new_thread(clientthread,(conn,addr))	

conn.close()
server.close()