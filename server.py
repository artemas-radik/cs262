import socket
import select
import sys
from _thread import *
from enum import Enum

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

def encode(response, message):
    return response.value.to_bytes(1, 'big') + len(message).to_bytes(2, 'big') + message.encode('ascii')

def decode(buffer):
	print('decode triggered')
	match buffer[0]:
		case Payload.register.value:
			print('reg triggered')
			username = buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')
			password = buffer[int.from_bytes(buffer[1:3],'big')+3:].decode('ascii')
			print(f"{username} {password}")
		case Payload.login.name:
			username = buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')
			password = buffer[int.from_bytes(buffer[1:3],'big')+3:].decode('ascii')
		case Payload.deleteacc.name:
			pass
		case Payload.accdump.name:
			pass
		case Payload.accfilter.name:
			wildcard = buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')
		case Payload.message.name:
			to = username = buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')
			content = buffer[int.from_bytes(buffer[1:3],'big')+3:].decode('ascii')
		case _:
			print("[FAILURE] Incorrect command usage.")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
	print ("Correct usage: script, IP address, port number")
	exit()

IP_address = str(sys.argv[1])

Port = int(sys.argv[2])
server.bind((IP_address, Port))
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
	suc(conn, "Welcome to this chatroom!")
	while True:
			try:
				message = decode(conn.recv(4096))
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