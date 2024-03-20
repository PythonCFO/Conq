import pygame
from network import Network
from player import Player
import time
import threading

width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

p = Player("Jay")  #Create this client-side Player object

def client_connection_thread():  # Create a Thread for each new Client Socket Connection
    conn = Network()  #Esablish Client's socket and connect it to the Server

    def connect(self, host, port):
        self.sock.connect((host, port))

    #Socket send data to Server
    def mysend(self, msg):
        totalsent = 0
        sent = self.sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

    #Socket receive data from Server
    def myreceive(self):
        bytes_recd = 0
        chunk = self.sock.recv(2048)
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunk)

    # Heartbeat
    while True:
        Heartbeat_Response = conn.send("Heartbeat from " + str(p.name)) #Send heartbeat to Server and save response
        if Heartbeat_Response == "ACK": 
            print("Sent Hearbeat : Server ACK")
        t_end = time.time() + 5 #Pause 5 seconds until next heartbeat / This delay is blocking (bad)
        while time.time() < t_end:   # Blocking loop.  Need to include other Client work
            pass

def redrawWindow(win):
    win.fill((255,255,255))
    p.draw(win)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    #Spin up a thread to run the client's Socket connection
    socket_thread = threading.Thread(target=client_connection_thread, daemon=True)     
    socket_thread.start()

    print("Starting Client process")  #All Client processing happens within this loop
    while True:
        clock.tick(60) #Max 60 ticks per second - possibly not needed

        #Get info on game status (such as other players state)
        #update() - draws the other player in the example

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        #print("Calling move")
        p.move()  #Perform local actions. But once per loop iteration?
        redrawWindow(win) #Send args needed to redraw local window.


main()
