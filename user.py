import uuid
import pickle
from game import Command 

class User:
    def __init__(self):
        self.userID = str(uuid.uuid1())[:8]
        self.name = "TEMP"
        self.connected = False
        #print(f"User: {self.userID} as {self.name}")

    def join(self, user):
        global send_queue, recv_queue, ack_queue

        print(f"Sending JOIN request to Server")
        print(f"{user.userID} join request")  #Request a formal User object from Server

        print("Queues: " + str(send_queue.qsize())+ str(ack_queue.qsize())+ str(recv_queue.qsize()))
        try:
            send_queue.put(Command(user.userID, "JOIN", user.userID + " join request"))  #Request a formal User object from Server

            #Commenting out the next Cmd; Receipt should be caught by revc_loop
            #user_cmd = pickle.loads(self.client.recv(2048))  #Receive USER object from Server <= not doing this now...
            
            #Should split the following into 2 Server interactions.
            #First is an ACK to joining.
            #Second, Server sends a USER command, to update the uuid with Server devised number
            
            #Trying an alt way; commenting out the next 3 lines...
            #user = user_cmd.cmd_data
            #print(f"{user_cmd.command} : {user_cmd.cmd_data}")
            #print(user.name)

            #EITHER: Loop here waiting for response, or use Queues for the Server response.
            #data = pickle.loads(self.client.recv(2048))  #Receive ACK from Server
            #print(f"{data.command}: {data.cmd_data}") 
            #return pickle.loads(self.client.recv(2048))  #Receive USER object from Server
            return #data
        except:
            print("Failed to join the game")
            return

