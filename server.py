import socket
import select
import sys
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
			pass

		case Payload.message.value:
			to = username = buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')
			content = buffer[int.from_bytes(buffer[1:3],'big')+3:].decode('ascii')
		case _:
			print("[FAILURE] Incorrect command usage.")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
	suc(conn, "Welcome to this chatroom!")
	while True:
			try:
				data = conn.recv(4096)
				if not data: break
				message = decode(data, conn)
				if message:
					print ("<" + addr[0] + "> " + message.strip())
					message_to_send = "<" + addr[0] + "> " + message
					broadcast(message_to_send, conn)
				else:
					remove(conn)
			except:
				continue

def broadcast(message, connection):
	for client in list_of_clients:
		if client!=connection:
			try:
				nms(client, "testuser", message)
			except:
				client.close()
				remove(client)

def remove(connection):
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

while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)
	print (addr[0] + " connected")
	start_new_thread(clientthread,(conn,addr))	

conn.close()
server.close()