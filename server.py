import socket
import select
import sys
from _thread import *
from enum import Enum

accounts = {}

class Account:
	def __init__(self, password):
		self.password = password

def interpret(buffer, socket):
	command = buffer.decode('utf-8').split(' ')
	match command[0]:

		case 'register':
			if command[1] in accounts.keys():
				socket.send("Username already registered.".encode('utf-8'))
				return
			accounts[command[1]] = Account(command[2])
			socket.send(f'Registered {command[1]}.'.encode('utf-8'))

		case 'login':
			if command[1] in accounts.keys():
				if accounts[command[1]].password == command[2]:
					accounts[command[1]].socket = socket
					socket.send(f'Authenticated {command[1]}.'.encode('utf-8'))
					return
				else:
					socket.send(f'Wrong password.'.encode('utf-8'))
			socket.send(f'Username not found.'.encode('utf-8'))

		case 'deleteacc':
			for account in accounts.keys():
				if accounts[account].socket == socket:
					del accounts[account]
					socket.send(f'Account deleted.')
					return
			socket.send(f'Not authenticated.')

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
			try:
				for username in accounts:
					if accounts[username].socket == socket:
						accounts[command[1]].socket.send(f'<{username}> {" ".join(command[2:])}'.encode('utf-8'))
					socket.send('[FAILURE] Unauthenticated.'.encode('utf-8'))
			except:
				print("client offline!")

		case _:
			socket.send('[FAILURE] Incorrect command usage.'.encode('utf-8'))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
server.listen(100)

def clientthread(conn):
	while True:
		try:
			data = conn.recv(4096)
			if not data: break
			interpret(data, conn)
		except:
			continue

while True:
	conn, addr = server.accept()
	print (addr[0] + " connected")
	start_new_thread(clientthread,(conn,))