import pygame as pg
import time
import threading
from network import Network
from player import Player
import geo

pg.init()
pg.mixer.init()
pg.font.init()
width = 1280
height = 720
win_size = pg.Vector2(width, height)
win = pg.display.set_mode(win_size, pg.RESIZABLE)
pg.display.set_caption("Risk Client")

clock = pg.time.Clock()

board = geo.World("Proto", proto_r=4, proto_c=5)  # Proto creates a hex grid test board
p = Player("Jay")  #Create a client-side Player object

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
        msg = self.sock.recv(2048)
        if msg == b'':
            raise RuntimeError("socket connection broken")
        bytes_recd = bytes_recd + len(msg)
        return b''.join(msg)

    # Heartbeat
    while True:
        Heartbeat_Response = conn.send("Heartbeat from " + str(p.name)) #Send heartbeat to Server and save response
        if Heartbeat_Response == "ACK": 
            print("Sent Hearbeat : Server ACK")
        t_end = time.time() + 5 #Pause 5 seconds until next heartbeat / This delay is blocking (bad)
        while time.time() < t_end:   # Blocking loop.  Need to include other Client work
            pass

def main():
    run = True
    clock = pg.time.Clock()

    #Spin up a thread to run the client's Socket connection
    socket_thread = threading.Thread(target=client_connection_thread, daemon=True)     
    socket_thread.start()

    print("Starting Client process")  #All Client processing happens within this loop
    while True:
        clock.tick(60)
        win.fill((0, 0, 0))
        game_events()
        game_update()
        game_draw()
        board.draw(win)
        pg.display.update()

        #redrawWindow(win) #Send args needed to redraw local window.

def game_events() -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                playing = False
                pg.quit()
        if event.type == pg.VIDEORESIZE:
            # There's some code to add back window content here.
            surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)

def game_update() -> None:
    now = pg.time.get_ticks()
    board.update()
    #p.update("place_units")  #temp used 'place_unit'

def game_draw() -> None:
    board.draw(win)

main()
