import config
import threading
import socket, errno
import queue
from game import Command
import pickle
from user import User

#Establish I/O threads for each Client: send_loop, recv_loop

def send_loop(conn: socket.socket, userID, send_queue, recv_queue):
    send_lock = threading.Lock()   #Define the lock but do not activate yet
    while config.users[userID].connected:
        send_lock.acquire()
        #if send_queue.qsize()>0:
        if config.send_queues[userID].qsize()>0:
            message = config.send_queues[userID].get()   #JOIN,Hello
            print(f"Sending: {message.userID}: {message.command}: {message.cmd_data}")
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
    print(f"Exiting {userID} send_loop thread")
    config.users[userID].connected == False


def recv_loop(conn: socket.socket, userID, send_queue, recv_queue):
    recv_lock =  threading.Lock()  #Define the lock but do not activate yet
    while config.users[userID].connected:  
        try:
            message = pickle.loads(conn.recv(4096))  #Get any inbound messages
            # Should validate incoming userID matches Server system of record
        except socket.error as e:
            print(e)
            print("Socket error in recv_loop")
            config.users[userID].connected = False
            message = ""
            break
        except:
            config.users[userID].connected = False
            print("Socket error in recv_loop")
            try:
                config.users[userID].connected = False
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
                    print(f"Receiving: {str(message.command)}: {message.cmd_data}; Pushing to recv_queue")
                    recv_queue.put(message) #Then push onto the Server's recv_queue to process
            else: 
                print(f"Badly formatted command from client {userID}")
                #Let the Connection Mgr do the removal of players.
            recv_lock.release()
        message = ""
    print(f"Exiting {userID} recv_loop thread")
    config.users[userID].connected == False

def remove_player(user):
    #DEPRECATED:  Not sure I will use this remove_player function any longer
    for u in config.users:
        i = config.users.index(u)
        if config.users[i] == user:
            #users.remove(u)
            config.users.pop(i)
            config.send_queues.pop(i)
            if config.VERBOSE: print("User found and removed")
    print(f"Removing user: {user.userID}")
    print("Active Players:")
    if len(config.users)>0:
        for u in config.users:
            i = config.users.index(u)
            print(f"   {u.name} - {config.send_queues[i][0]} {config.send_queues[i][3][0]}:{config.send_queues[i][3][1]}")
            #print(f"   {u.name} - {config.send_queues[i][0]} {config.send_queues[i][3][0]}:{config.send_queues[i][3][1]}  {recv_thread.name} {send_thread.name}")
    else:
            print(f"   none")
    print("Active Threads:")
    for t in threading.enumerate():
        print(f"   {t.name}")
