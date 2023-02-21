import socket
import select
import sys
from _thread import *
from enum import Enum

accounts = {}

class Account:
	def __init__(self, password):
		self.password = password
		self.message_queue = []
	

def interpret(buffer, socket):
	command = buffer.decode('utf-8').split(' ')
	match command[0]:

		case 'register':
			if command[1] in accounts.keys():
				socket.send("Username already registered.".encode('utf-8'))
				return
			accounts[command[1]] = Account(command[2])
			socket.send(f'Registered {command[1]}.'.encode('utf-8'))
			return

		case 'login':
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

		case 'deleteacc':
			for account in accounts.keys():
				try:
					if accounts[account].socket == socket:
						del accounts[account]
						socket.send(f'Account deleted.'.encode('utf-8'))
						return
				except:
					pass
			socket.send(f'Not authenticated.'.encode('utf-8'))

		case 'accdump' | 'accfilter':
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

		case 'message':
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

		case _:
			socket.send('[FAILURE] Incorrect command usage.'.encode('utf-8'))
			return
	#socket.send('[FAILURE] Incorrect command usage.'.encode('utf-8'))

def clientthread(conn):
	while True:
		try:
			data = conn.recv(4096)
			if not data: 
				for username in accounts:
					if accounts[username].socket == conn:
						accounts[username].socket = None
				break
			interpret(data, conn)
		except:
			#conn.send('[FAILURE]'.encode('utf-8'))
			continue

if __name__ == "__main__":
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	IP_address = str(sys.argv[1])
	Port = int(sys.argv[2])
	server.bind((IP_address, Port))
	server.listen(100)

	while True:
		conn, addr = server.accept()
		print (addr[0] + " connected")
		conn.send('Connected!'.encode('utf-8'))
		start_new_thread(clientthread,(conn,))
