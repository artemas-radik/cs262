import socket, select, sys
from _thread import *
import threading
import uuid, pickle, csv, time

#TODO: handle case "Connection!"
    #ie guid == -1

#TODO: store guids of all messages ever sent, on clients

#NOTE: we're currently rewriting pending file upon every delete


def set_timer(guid, pending, pending_file, servers, serversLock):
    time.sleep(10) #allowed lag time
    with serversLock:
        if guid in pending: #implies a server failed
            cpy = servers.copy()
            for s in cpy:
                #remove all failed servers
                if s not in pending[guid]: servers.remove(s)
        
        try:
            #pop from dict
            md = pending.pop(guid)
            #remove from file
            open(pending_file, 'w').close() #flush pending_file
            with open (pending_file, 'w') as pending_log:
                fieldnames = ['guid', 'msg']
                csvwriter = csv.DictWriter(pending_log, fieldnames=fieldnames)
                csvwriter.writeheader()
                for id in pending:
                    csvwriter.writerow({'guid':id, 'msg':pending[id]['msg']})
            
            #print ack message
            print(pending[guid]['ack'])
            #if send_in_fut:
            if md['send_in_fut']:
                for s in servers:
                    m = {'guid':guid, 'msg':md['msg'].encode('utf-8')}
                    pickled = pickle.dumps(m)
                    s.send(pickled)
        except:
            pass

if __name__ == "__main__":
    num_servers = 3

    servers = set([socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(num_servers)])
    serversLock = threading.Lock()

    #initialize client state variables
    ip = str(sys.argv[1])
    ports = [int(sys.argv[i+2]) for i in range(num_servers)]

    base = "/Users/swatigoel/Dropbox/college/cs262/cs262/"
    pending_file = base + str(sys.argv[num_servers+2]) #requests which user "sent", but has not yet received full acknowledgement for 
        #if crash, client once again waits for confirmation from all servers (slightly inefficient, but cleaner code) 
        #row = guid, message
    pending = {} #msg = message sent/to be sent to server, ack = acknowledgement to be printed on client, ack_servers = servers which have confirmed receipt, send_in_fut = bool flag, determined behavior upon total ack

    #fill pending
    with open (pending_file, 'r') as pending_log:
        csvreader = csv.DictReader(pending_log)
        for row in csvreader:
            pending[row['guid']] = {'msg':row['msg'], 'ack':'', 'ack_servers':set(), 'send_in_fut':False}

    #connect to servers
    servers_lst = list(servers)
    for i in range(num_servers):
        servers_lst[i].connect((ip, ports[i]))

    #attempt send all pending_msgs
    #TODO: DO NOT SEND ACK MESSAGES!!
    for id in pending:
        m = {'guid': id, 'msg': pending[id]['msg'].encode('utf-8')}
        pickled = pickle.dumps(m)
        for server in servers_lst:
            server.send(pickled)
        
    #listen for messages
    while True:
        sockets_list = [sys.stdin] + list(servers)
        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
        for socks in read_sockets:
            #message received from server
            if socks in servers:
                data = socks.recv(4096)
                if (data == ''): 
                    pass #NOTE: assumption = timeout will shut down server in this case
                msgDict = pickle.loads(data)

                if msgDict['guid'] not in pending:
                    print("adding to pending:", msgDict['guid'], msgDict['msg'].decode('utf-8'))
                    #in this case, server initiated message, not client
                    #implies dictionary pending does not need to be persistent on client
                    pending[msgDict['guid']] = {'msg':"acknowledged", 'ack':msgDict['msg'].decode('utf-8'), 'ack_servers':set([socks]), 'send_in_fut':True} #nobody else could be modifying this key yet, no lock needed
                    start_new_thread(set_timer,(msgDict['guid'], pending, pending_file, servers, serversLock))
                else:
                    pending[msgDict['guid']]['ack'] = msgDict['msg'].decode('utf-8') #atomic operations, no lock needed
                    pending[msgDict['guid']]['ack_servers'].add(socks)
                    #print("adding server to pending:", msgDict['guid'], len(pending[msgDict['guid']]['ack_servers']))
                
                if servers.issubset(pending[msgDict['guid']]['ack_servers']): #all servers have ack receipt/sent message
                    message = print(msgDict['msg'].decode('utf-8'), "from: ", socks.fileno()) 
                    with serversLock:
                        md = pending.pop(msgDict['guid'])
                        #send ack message, if needed
                        if md['send_in_fut']:
                            for s in servers:
                                m = {'guid':msgDict['guid'], 'msg':md['msg'].encode('utf-8')}
                                pickled = pickle.dumps(m)
                                s.send(pickled)
                        open(pending_file, 'w').close() #flush pending_file
                        with open (pending_file, 'w') as pending_log:
                            fieldnames = ['guid', 'msg']
                            csvwriter = csv.DictWriter(pending_log, fieldnames=fieldnames)
                            csvwriter.writeheader()
                            for id in pending:
                                csvwriter.writerow({'guid':id, 'msg':pending[id]['msg']})
                                    
            #command received from user
            else:
                l = sys.stdin.readline().strip()
                guid = uuid.uuid4()
                m = {'guid': guid, 'msg': l.encode('utf-8')}
                pickled = pickle.dumps(m)

                #at this point, no other threads can modify this guid, implies no lock needed
                pending[guid] = {'msg':l, 'ack':'', 'ack_servers':set(), 'send_in_fut':False}
                with open (pending_file, 'a') as messages_log:
                    fieldnames = ['guid', 'msg']
                    csvwriter = csv.DictWriter(messages_log, fieldnames=fieldnames)
                    if messages_log.tell() == 0: csvwriter.writeheader()
                    csvwriter.writerow({'guid': guid, 'msg': l})
                start_new_thread(set_timer,(guid, pending, pending_file, servers, serversLock))
                for server in servers:
                    server.send(pickled)

#Client A --> Server
#if system crashes before message is processed client-side, nothing we can do
#if system crashes after message is sent but before message is processed, pending_messages on disk --> message resent
#if system crashes after message is processed by server but before ack is sent to client --> handled server side
    #client might also resend message, but server keeps tracks of guids, so this is fine
#if system crashes after ack is sent to client, but before ack is processed by client
    #pending_messages --> resent

#Server --> Client B
#if system crashes after message sent but before message removed from pending
    #server resends
#if system crashes after message sent but before client sends back ack
    #server resends (still in some pending apparatus)
#if system crashes after ack received by server, but before server removes from pending
    #server resends, and client is keeping track of guids, so no harm done