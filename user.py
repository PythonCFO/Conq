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
            return #data
        except:
            print("Failed to join the game")
            return

