import socket
import select
import sys
from _thread import *
from enum import Enum

# This is a hashmap/dictionary that stores a table of usernames that map to Account objects.
accounts = {}

# Each Account object password, message_queue, socket. The password lets the account log in after terminating a session. The message_queue is used when an account does not have an active socket and messages need to be stored for later delivery. The socket object denotes the Account's current associated object. If it is None, this means the client is currently disconnected. A client can only connect one session at a time.
class Account:
	def __init__(self, password):
		self.password = password
		self.message_queue = []
	
# This function interprets a transfer buffer that came in over a given socket.
def interpret(buffer, socket):
	command = buffer.decode('utf-8').split(' ')
	match command[0]: # command[0] maps to commands in our documentation, this is basically an opcode.
		case 'register': # register command. command[1] is the username, comamnd[2] is the password.
			if command[1] in accounts.keys():
				socket.send("Username already registered.".encode('utf-8'))
				return
			accounts[command[1]] = Account(command[2])
			socket.send(f'Registered {command[1]}.'.encode('utf-8'))
			return

		case 'login': # login command. command[1] is the username, comamnd[2] is the password.
			for u in accounts.keys():
				try:
					if accounts[u].socket == socket:
						socket.send("Ma'am, you are already logged in.".encode('utf-8'))
						return
				except:
					pass
			if command[1] in accounts.keys():
				if accounts[command[1]].password == command[2]:
					try:
						if accounts[command[1]].socket:
							socket.send("Max devices which can login at once: 1.".encode('utf-8'))
							return
					except:
						pass
					accounts[command[1]].socket = socket
					socket.send('\n'.join([f'Authenticated {command[1]}.'] + accounts[command[1]].message_queue).encode('utf-8'))
					accounts[command[1]].message_queue = []
					return
				else:
					socket.send(f'Wrong password.'.encode('utf-8'))
			socket.send(f'Username not found.'.encode('utf-8'))

		case 'deleteacc': # deleteacc command. authentication required.
			for account in accounts.keys():
				try:
					if accounts[account].socket == socket:
						del accounts[account]
						socket.send(f'Account deleted.'.encode('utf-8'))
						return
				except:
					pass
			socket.send(f'Not authenticated.'.encode('utf-8'))

		case 'accdump' | 'accfilter': # accdump/accfilter commands. these are combined because an accdump is equivalent to an accfilter with an empty wildcard.
			if accounts:
				dump = 'Users: '
				for account in accounts:
					if command[0] == 'accdump' or command[1] in account:
						dump += f'{account}, '
				socket.send((dump[:-2]+'.').encode('utf-8'))
				return
			else:
				socket.send('No accounts found.')
				return

		case 'message': # message command. command[1] is the target username, command[2:] is the message content (we join these into one string). authentication required. if try to deliver message to account that isn't in a current session, then it gets queued on the account object.
			logged_in = False
			uname = "Guest"
			if command[1] not in accounts:
				socket.send("User dne.".encode('utf-8'))
				return
			try:
				for username in accounts:
					if accounts[username].socket == socket:
						logged_in = True
						uname = username
						accounts[command[1]].socket.send(f'<{username}> {" ".join(command[2:])}'.encode('utf-8'))
						return
			except:
				if (not logged_in):
					socket.send("Kindly log in.".encode('utf-8'))
					return
				socket.send("Client offline!".encode('utf-8'))
				accounts[command[1]].message_queue.append(f'<{uname}> {" ".join(command[2:])}')

		case _: # uninterpretable, so send error.
			socket.send('[FAILURE] Incorrect command usage.'.encode('utf-8'))
			return

# This function represents a client thread. Each client gets once.
def clientthread(conn):
	while True:
		try:
			data = conn.recv(4096)
			if not data: # this runs when a client ctrl-c's, so we make sure to note that on their account object, if they have one.
				for username in accounts:
					if accounts[username].socket == conn:
						accounts[username].socket = None
				break
			interpret(data, conn)
		except:
			continue

# Run at startup.
if __name__ == "__main__":
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try: 
		IP_address = str(sys.argv[1])
		Port = int(sys.argv[2])
	except:
		IP_address = "52.152.216.212"
		Port = 5000
	server.bind((IP_address, Port))
	server.listen(100)

	while True: # infinite loop to continually accept new clients
		conn, addr = server.accept()
		print (addr[0] + " connected")
		conn.send('Connected!'.encode('utf-8'))
		start_new_thread(clientthread,(conn,))
