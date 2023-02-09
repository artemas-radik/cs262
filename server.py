import socket
import select
import struct
import sys
from _thread import *

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
				message = conn.recv(2048).decode('utf-8')
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
	client.send(struct.pack('B256s272x', 7, message.encode('ascii')))

def nms(client, from_username, content):
	client.send(struct.pack('B16s512s', 8, from_username.strip().encode('ascii'), content.strip().encode('ascii')))

while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)
	print (addr[0] + " connected")
	start_new_thread(clientthread,(conn,addr))	

conn.close()
server.close()