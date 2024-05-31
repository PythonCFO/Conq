import threading
import socket
import queue
from game import Command
import pickle
from user import User
from gamedb import ref
import time

def socket_mgr(users, send_queues, recv_queue):
    global network_provisioned        
    server = "localhost"
    port = 5556
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ref.child("logging").push("Binding Socket to server port.")
    while True:
        try:
            s.bind((server, port))
            network_provisioned = True
            break
        except socket.error as e:
            print(".", end='', flush=True)
            time.sleep(1)
    s.listen(10)  # Listen (blocking) for Socket connections
    ref.child("logging").push("Socket_mgr started - listening for connections")
    total_conns = 0
    while True:  
        conn, addr = s.accept()  #Blocking wait for user to connect via Socket
        ref.child("logging").push("Connecting...")
        total_conns += 1
        user = User()  #Server creates a user object
        users[user.userID] = user  #Add new user to the Dictionary
        users[user.userID].name = "Player_" + str(total_conns)  #Name the user
        users[user.userID].connected = True  #Enable comms with this user
        
        send_queues[user.userID] = queue.Queue() #Add new queue to send_queues Dictionary

        ref.child("logging").push("Starting send_loop and recv_loop threads for: " + user.name)
        recv_thread = threading.Thread(name=str(user.userID)+"_recv", target=recv_loop, args=(conn, user.userID, users, send_queues[user.userID], recv_queue), daemon=True).start()
        send_thread = threading.Thread(name=str(user.userID)+"_send", target=send_loop, args=(conn, user.userID, users, send_queues[user.userID]), daemon=True).start()

        #Welcome the new user
        send_queues[user.userID].put(Command(user.userID, "ACK", "Welcome to Conq!"))
        send_queues[user.userID].put(Command(user.userID, "WHOAMI", user))  #Send "server created" User obj

        print(f"New user: {user.userID}")
        print("Active Users:")
        for u in users.keys():
            if users[u].connected == True:
                print(f"   {users[u].name} - {users[u].userID}") 
        print("Active Threads:")
        for t in threading.enumerate():
            print(f"   {t.name}")

def send_loop(conn: socket.socket, userID, users, send_queue):
    send_lock = threading.Lock()   #Define the lock but do not activate yet
    while users[userID].connected:
        send_lock.acquire()
        if send_queue.qsize()>0:
            message = send_queue.get()   #JOIN,Hello
            ref.child("logging").push(f"Sending: {message.userID}: {message.command}: {message.cmd_data}")
            try:
                conn.send(pickle.dumps(message))
            except socket.error as e:
                print(e)
                print("Socket error in recv_loop")
            except:
                #Need to pass notification of lost connection to the SocketMgr
                print("Socket error in recv_loop")
                break
            message = ""
        send_lock.release()
    ref.child("logging").push(f"Exiting {userID} send_loop thread")
    users[userID].connected == False

def recv_loop(conn: socket.socket, userID, users, send_queue, recv_queue):
    recv_lock =  threading.Lock()  #Define the lock but do not activate yet
    while users[userID].connected:  
        try:
            message = pickle.loads(conn.recv(4096))  #Get any inbound messages
            # Should validate incoming userID matches Server system of record
        except socket.error as e:
            print(e)
            print("Socket error in recv_loop")
            users[userID].connected = False
            message = ""
            break
        except:
            users[userID].connected = False
            print("Socket error in recv_loop")
            try:
                users[userID].connected = False
            except:
                pass
            message  = ""
            break
        if message != "":
            recv_lock.acquire()
            if type(message) == Command:
                if message.command == "HBT": send_queue.put(Command(userID, "ACK", "HBT received"))
                elif message.command == "ACK": pass  #Should tie-off the original Cmd was ACK'd
                else: 
                    ref.child("logging").push(f"Receiving: {str(message.command)}: {message.cmd_data}; Pushing to recv_queue")
                    recv_queue.put(message) #Then push onto the Server's recv_queue to process
            else: 
                ref.child("logging").push(f"Badly formatted command from client {userID}")
                #Let the Connection Mgr do the removal of players.
            recv_lock.release()
        message = ""
    ref.child("logging").push(f"Exiting {userID} recv_loop thread")
    users[userID].connected == False

