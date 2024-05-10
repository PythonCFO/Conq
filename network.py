import client_config
import socket
from game import Command
import time
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            print(f"Connecting to Server {self.addr}")
            self.client.connect(self.addr) #Establish Socket connection to Server
            print("Connected!")
            client_config.user.connected = True
            data =  pickle.loads(self.client.recv(2048))  #Wait for an ACK
            print(f"{data.command}: {data.cmd_data}") #"Welcome to Cong! message..."
            return #user
        except socket.error as e:
            print(e)
            return ("Socket Exception at n.connect()" + str(e))
        except:
            print(f"Connection to Server failed")
            return False


    #Socket send data to Server
    def send(self, data):  #Client send function
        try:
            self.client.send(pickle.dumps(data))
            return True
        except socket.error as e:
            return False
        except:
            print("Socket Send() failed")
            return False

    #Socket receive data from Server
    def socket_recv(self):
        try:
            data = self.client.recv(2048)   #Wait for inbound msg
            return True
        except socket.error as e:
            print(e)
            return False
        except:
            print("Socket socket_recv() failed")
            return False
        
        if data != b'':
            message = pickle.loads(data)
            return message
        else:
            print("Connection broken; Goodbye")
            #TODO Need to handle lost connection!!
                #E.g. establish a reconenction process
                #E.g. establish a FLAG to pause future network requests
                #Be aware this could be due to "Server down or unavailable"!
                    #Not just due to client code issue

def network_check(client, userID):
    global HBT_time
    global send_lock
    global send_queue
    print(".", end='', flush=True)
    print(userID)
    if time.time() >= HBT_time:
        hbt_cmd = Command(userID.userID, "HBT", "Ready to play")
        send_lock.acquire()
        send_queue.put(hbt_cmd)  #Or use the Send Queue to send the command...
        send_lock.release()
        HBT_time = time.time() + 5 #Pause 5 seconds until next heartbeat / This delay is blocking (bad)
        print(time.time(), HBT_time)

