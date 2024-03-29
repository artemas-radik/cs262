import socket, select, sys, os, uuid, pickle, csv, time, threading
from _thread import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def set_timer(guid, pending, pending_file, servers, serversLock):
    time.sleep(10) #allowed lag time
    with serversLock:
        if guid in pending: #implies a server failed
            cpy = servers.copy()
            for s in cpy:
                #remove all failed servers
                if s not in pending[guid]: 
                    servers.remove(s)
        try:
            #pop from dict
            md = pending.pop(guid)
            #remove from file
            open(pending_file, 'w').close()
            with open (pending_file, 'w') as pending_log:
                fieldnames = ['guid', 'msg']
                csvwriter = csv.DictWriter(pending_log, fieldnames=fieldnames)
                csvwriter.writeheader()
                for id in pending:
                    csvwriter.writerow({'guid':id, 'msg':pending[id]['msg']})
                    csvwriter.writerow({'guid':id, 'msg':pending[id]['msg']})
            
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

    ips = ["20.121.21.153", "20.168.51.12", "20.63.58.144"]
    ports = [5000, 5000, 5000]
    pending_file = "db-client.csv"

    if len(sys.argv) > 1:
        #initialize client state variables
        ips =  [str(sys.argv[1]) for _ in range(num_servers)]
        ports = [int(sys.argv[i+2]) for i in range(num_servers)]
        pending_file = os.getcwd() + str(sys.argv[num_servers+2]) #requests which user "sent", but has not yet received full acknowledgement for 
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
        try:
            servers_lst[i].connect((ips[i], ports[i]))
        except:
            print(bcolors.FAIL + f"Server [{ips[i]}:{ports[i]}] offline." + bcolors.ENDC)
            servers.remove(servers_lst[i])
            pass

    #attempt send all pending_msgs
    #do not send pending acknowledgements
    for id in pending:
        if pending[id]['send_in_fut']: continue
        m = {'guid': id, 'msg': pending[id]['msg'].encode('utf-8')}
        pickled = pickle.dumps(m)
        for server in servers_lst:
            server.send(pickled)
        
    #listen for messages
    end_test = False
    while True:
        sockets_list = [sys.stdin] + list(servers)
        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
        for socks in read_sockets:
            #message received from server
            if socks in servers:
                data = socks.recv(4096)
                if (len(bytes(data)) == 0):
                    servers.remove(socks)
                    print(bcolors.FAIL + f"Server [{socks.getpeername()[0]}:{socks.getpeername()[1]}] offline." + bcolors.ENDC)
                    break
                
                msgDict = pickle.loads(data)

                if msgDict['guid'] not in pending:
                    #in this case, server initiated message, not client
                    #implies dictionary pending does not need to be persistent on client
                    pending[msgDict['guid']] = {'msg':"acknowledged", 'ack':msgDict['msg'].decode('utf-8'), 'ack_servers':set([socks]), 'send_in_fut':True} #nobody else could be modifying this key yet, no lock needed
                    start_new_thread(set_timer,(msgDict['guid'], pending, pending_file, servers, serversLock))

                else:
                    pending[msgDict['guid']]['ack'] = msgDict['msg'].decode('utf-8') #atomic operations, no lock needed
                    pending[msgDict['guid']]['ack_servers'].add(socks)
                
                if servers.issubset(pending[msgDict['guid']]['ack_servers']): #all servers have ack receipt/sent message
                    message = print(bcolors.BOLD + bcolors.OKGREEN + f"[{socks.getpeername()[0]}:{socks.getpeername()[1]}]" + bcolors.ENDC, msgDict['msg'].decode('utf-8')) 
                    with serversLock:
                        md = pending.pop(msgDict['guid'])
                        #send ack message, if needed
                        if md['send_in_fut']:
                            for s in servers:
                                m = {'guid':msgDict['guid'], 'msg':md['msg'].encode('utf-8')}
                                pickled = pickle.dumps(m)
                                s.send(pickled)
                        open(pending_file, 'w').close()
                        with open (pending_file, 'w') as pending_log:
                            fieldnames = ['guid', 'msg']
                            csvwriter = csv.DictWriter(pending_log, fieldnames=fieldnames)
                            csvwriter.writeheader()
                            for id in pending:
                                csvwriter.writerow({'guid':id, 'msg':pending[id]['msg']})
                                    
            #command received from user
            else:
                if end_test: continue
                l = sys.stdin.readline().strip()
                if not l:
                    end_test = True
                    break
                #print("debug", l)
                guid = str(uuid.uuid4())
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