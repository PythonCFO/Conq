from network import Network
import time 

clientNumber = 0

class Player():
    def __init__(self, name):
        #Basic Client-side Player initialization can be done here during initialization
        self.name = name

def main():
    p = Player("Jay")  #Create this client-side Player object
    conn = Network()  #Esablish Client's socket and connect it to the Server

    print("Starting Client Loop")  #All Client processing happens within this loop
    while True:
        Heartbeat_Response = conn.send("Heartbeat from " + str(p.name)) #Send heartbeat to Server and save response
        if Heartbeat_Response == "ACK": 
            print("Snd Hearbeat : Server ACK")
        t_end = time.time() + 5 #Pause 5 seconds until next heartbeat / This delay is blocking (bad)
        while time.time() < t_end:
            pass

main()
