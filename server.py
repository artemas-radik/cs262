import socket
import select
import sys
from _thread import *
import threading
import csv, pickle
from enum import Enum

#TODO: store state of system (accounts + message queue) to a file
#TODO: store message_queue in file *until* acknowledgement received from client
	#ie, don't delete from message_queue until client has acknowledged recepit 

#NOTE: do we need every if/else branch to contain a return statement?
#NOTE: check login a '' behavior (caused a system malfunction in design exercise 1)

# This is a hashmap/dictionary that stores a table of usernames that map to Account objects.
accounts = {}
pending = {} 
pendingLock = threading.Lock()

# Each Account object password, message_queue, socket. The password lets the account log in after terminating a session. The message_queue is used when an account does not have an active socket and messages need to be stored for later delivery. The socket object denotes the Account's current associated object. If it is None, this means the client is currently disconnected. A client can only connect one session at a time.
class Account:
	def __init__(self, password):
		self.password = password
		self.message_queue = []

def send_msg(socket, guid, msg):
	response = {'guid': guid, 'msg': msg.encode('utf-8')}
	pickled = pickle.dumps(response)
	socket.send(pickled)
	
# This function interprets a transfer buffer that came in over a given socket.
def interpret(buffer, guid, socket):
	command = buffer.decode('utf-8').split(' ')
	match command[0]: # command[0] maps to commands in our documentation, this is basically an opcode.
		case 'register': # register command. command[1] is the username, command[2] is the password.
			if len(command) <= 2:
				send_msg(socket, guid, "Invalid/missing password")
				return
			if command[1] in accounts.keys():
				send_msg(socket, guid, "Username already registered.")
				return
			accounts[command[1]] = Account(command[2])
			send_msg(socket, guid, f'Registered {command[1]}.')
			return

		case 'login': # login command. command[1] is the username, command[2] is the password.
			for u in accounts.keys():
				try:
					if accounts[u].socket == socket:
						send_msg(socket, guid, "You are already logged in.")
						return
				except:
					pass
			if command[1] in accounts.keys():
				if accounts[command[1]].password == command[2]:
					try:
						if accounts[command[1]].socket:
							send_msg(socket, guid, "Max devices which can login at once: 1.")
							return
					except:
						pass
					accounts[command[1]].socket = socket
					send_msg(socket, guid, '\n'.join([f'Authenticated {command[1]}.'] + accounts[command[1]].message_queue))
					#accounts[command[1]].message_queue = [] #MOVED TO 'acknowledge' case
					return
				else:
					send_msg(socket, guid, f'Wrong password.')
					return
			send_msg(socket, guid, f'Username not found, or incorrect command usage.')

		case 'deleteacc': # deleteacc command. authentication required.
			for account in accounts.keys():
				try:
					if accounts[account].socket == socket:
						del accounts[account]
						send_msg(socket, guid, f'Account deleted.')
						return
				except:
					pass
			send_msg(socket, guid, f'Not authenticated.')

		case 'accdump' | 'accfilter': # accdump/accfilter commands. these are combined because an accdump is equivalent to an accfilter with an empty wildcard.
			if accounts:
				dump = 'Users: '
				for account in accounts:
					if command[0] == 'accdump' or command[1] in account:
						dump += f'{account}, '
				send_msg(socket, guid, (dump[:-2]+'.'))
				return
			else:
				send_msg(socket, guid, 'No accounts found.')
				return

		case 'message': # message command. command[1] is the target username, command[2:] is the message content (we join these into one string). authentication required. if try to deliver message to account that isn't in a current session, then it gets queued on the account object.
			logged_in = False
			uname = "Guest"
			if command[1] not in accounts:
				send_msg(socket, guid, "User dne.")
				return
			try:
				for username in accounts:
					if accounts[username].socket == socket:
						logged_in = True
						uname = username
						with pendingLock:
							pending[guid] = {'dest':command[1]}
							with open (pending_file, 'a') as pending_log:
								fieldnames = ['guid', 'dest']
								csvwriter = csv.DictWriter(pending_log, fieldnames=fieldnames)
								if pending_log.tell() == 0: csvwriter.writeheader()
								csvwriter.writerow({'guid':guid, 'dest':command[1]})
						send_msg(accounts[command[1]].socket, guid, f'<{username}> {" ".join(command[2:])}')
						return
			except:
				if (not logged_in):
					send_msg(socket, guid, "Kindly log in.")
					return
				send_msg(socket, guid, "Client offline!")
				accounts[command[1]].message_queue.append(f'<{uname}> {" ".join(command[2:])}')
			
		case 'acknowledged':
			with pendingLock:
				md = pending.pop(guid)
				accounts[md['dest']].message_queue = [] #TODO: propagate to file
				open(pending_file, 'w').close() #flush pending_file
				with open (pending_file, 'w') as pending_log:
					fieldnames = ['guid', 'dest']
					csvwriter = csv.DictWriter(pending_log, fieldnames=fieldnames)
					csvwriter.writeheader()
					for id in pending:
						csvwriter.writerow({'guid':id, 'dest':pending[id]['dest']})
			return

		case _: # uninterpretable, so send error.
			send_msg(socket, guid, '[FAILURE] Incorrect command usage.')
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
			msgDict = pickle.loads(data)
			interpret(msgDict['msg'], msgDict['guid'], conn)
		except:
			continue

# Run at startup.
if __name__ == "__main__":
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#try: 
	IP_address = str(sys.argv[1])
	Port = int(sys.argv[2])
	"""except:
		IP_address = "52.152.216.212"
		Port = 5000"""
	
	base = "/Users/swatigoel/Dropbox/college/cs262/cs262/"
	pending_file = base + str(sys.argv[3])
	server.bind((IP_address, Port))
	server.listen(100)

	with open (pending_file, 'r') as pending_log:
		csvreader = csv.DictReader(pending_log)
		for row in csvreader:
			pending[row['guid']] = {'dest':row['dest']}

	while True: # infinite loop to continually accept new clients
		conn, addr = server.accept()
		print (addr[0] + " connected")

		m = {'guid': -1, 'msg': 'Connected!'.encode('utf-8')}
		pickled = pickle.dumps(m)
		conn.send(pickled)
		start_new_thread(clientthread,(conn,))


#persistence, server-side:

#Client A-->server, post command processed by server
#entire system crashes
	#client resends command to server, server *also* reexecutes command (this is redundant)
	#implies the server does not need to store commands triggered by client
#server fault handled by client
#server just needs to store the state of the system to files

#server-->Client B
#server is responsible for processing message acknowledgement
#Note: we do not need to implement "resend" functionality (already implemented in form of message_queue)
	#we just need to move emptying message_queue statement to case acknowledge