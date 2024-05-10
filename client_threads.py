import socket
import threading
from game import Command
import pickle

def send_loop(n, send_queue, recv_queue):
    send_lock = threading.Lock()
    print("Client send_loop Thread started")  #All Client processing happens within this loop   

    #TODO: (1:m) send msgs use randome userID. Use "ServerID" instead? 

    while True:
        send_lock.acquire()
        if send_queue.qsize()>0:
            message = send_queue.get()
            n.send(message)
            print(f"Sending: {str(message.command)}: {message.cmd_data}")
            message = ""
        send_lock.release()

def recv_loop(n, send_queue, recv_queue):
    recv_lock = threading.Lock()
    print("Client receive_loop Thread started")
    while True:
        try:
            message = pickle.loads(n.client.recv(4096))  #Get any inbound messages
        except socket.error as e:
            print(e)
            print("Socket error in recv_loop")
            #Consider adding: user.connected = False
            message = ""
            break
        except:
            print("Exception in recv_loop")
            #Agail consider: user.connected = False
            message  = ""
            break
        recv_lock.acquire()
        if type(message) == Command:  #Confirm whether msg is properly formed
            print(f"Receiving: {str(message.command)}: {message.cmd_data}")
            if message.command == "ACK": #send_queue may be waiting for success confirmation
                pass
            else:
                print(f"     Putting {message.command} command onto recv_queue")
                recv_queue.put(message) #Then push onto the incoming queue for processing
        else:  #Else abandon the bad incoming message
            print(f"Bad Message: {str(message)}")
        message = ""            
        recv_lock.release()


