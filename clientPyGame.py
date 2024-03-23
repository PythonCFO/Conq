import pygame as pg
import time
import threading
from network import Network
from player import Player
import geo
from gameplay import Command, Gameplay
import pickle

pg.init()
pg.mixer.init()
pg.font.init()
width = 1280
height = 720
win_size = pg.Vector2(width, height)
win = pg.display.set_mode((width, height))
pg.display.set_caption("Risk Client")
clock = pg.time.Clock()

board = geo.World("Proto", proto_r=4, proto_c=5)  # Proto creates a hex grid test board
p = Player("TBD")  #Create a client-side Player object

test_cmd = Command("name", p, ("My Test Name"))
c = Network

def client_connection_thread(c):  # Create a Thread for each new Client Socket Connection
    conn = Network()  #Esablish Client's socket and connect it to the Server
    c = conn

    #def connect(self, host, port):
    #    self.sock.connect((host, port))

    # Heartbeat
    while True:
        Heartbeat_Response = conn.send("test") #pickle.dumps(p.name)) #Send heartbeat to Server and save response
        if Heartbeat_Response == "ACK": 
            print("Sent Hearbeat : Server ACK")
        t_end = time.time() + 5 #Pause 5 seconds until next heartbeat / This delay is blocking (bad)
        while time.time() < t_end:   # Blocking loop.  Need to include other Client work
            pass

def redrawWindow(win):
    win.fill((255,255,255))
    p.draw(win)
    pg.display.update()

def main():
    run = True

    #Spin up a thread to run the client's Socket connection
    socket_thread = threading.Thread(target=client_connection_thread, daemon=True)     
    socket_thread.start()

    print("Starting Client process")  #All Client processing happens within this loop
    while True:
        clock.tick(60) #Max 60 ticks per second - possibly not needed
        win.fill((0,0,0))
        game_events(c)
        game_update()
        game_draw()
        board.draw(win)
        pg.display.update()

def game_events() -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                playing = False
                pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                print("Need to implement sending a test Command within clientPyGame")  #Testing sending a Comand to Server
                test_cmd = c.send("Heartbeat from " + str(p.name))
                print(test_cmd)
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
