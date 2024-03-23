from network import Network
import time 
import threading
from player import Player
from gameplay import Command, Gameplay


def main():
    p = Player("Jay")  #Create this client-side Player object
    conn = Network()  #Esablish Client's socket and connect it to the Server
    test_cmd = Command("name", p, ("My Test Name"))

    print("Starting Client Loop")  #All Client processing happens within this loop
    while True:
        Heartbeat_Response = conn.send("Heartbeat from " + str(p.name)) #Send heartbeat to Server and save response
        if Heartbeat_Response == "ACK": 
            print("Sent Hearbeat : Server ACK")
        t_end = time.time() + 5 #Pause 5 seconds until next heartbeat / This delay is blocking (bad)
        while time.time() < t_end:   # Blocking loop.  Need to include other Client work
            pass

main()
