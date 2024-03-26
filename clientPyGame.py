import pygame as pg
import time
import threading
from network import Network
from player import Player
import geo
from gameplay import Command, Gameplay
import pickle
import queue

pg.init()
pg.mixer.init()
pg.font.init()
width = 1280
height = 720
win_size = pg.Vector2(width, height)
win = pg.display.set_mode((width, height))
pg.display.set_caption("Risk Client")
clock = pg.time.Clock()
t_end = time.time() + 5

#Proto Board should be built by the SERVER!!!
board = geo.World("Proto", proto_r=4, proto_c=5)  # Proto creates a hex grid test board

'''
def client_connection_thread(netconn):  # Thread to make the Socket Connection to Server
    while True:
        netconn.send(Command(p.id, "HBT", "Ready to play" )) #pickle.dumps(p.name)) #Send heartbeat to Server and save response
        t_end = time.time() + 5 #Pause 5 seconds until next heartbeat / This delay is blocking (bad)
        while time.time() < t_end:   # Blocking loop.  Need to include other Client work
            pass
'''
netconn = Network()  #Esablish Client's socket and connect it to the Server
p = Player(netconn)  #Create this client-side Player object

send_queue = queue.Queue()
recv_queue = queue.Queue()
ack_queue = queue.Queue()
lock=threading.Lock()
send_lock=threading.Lock()
recv_lock=threading.Lock()
proc_lock=threading.Lock()

def send_loop():
    global netconn
    print("Client Send Thread Started")  #All Client processing happens within this loop   
    RTS = True  #Ready To Send - Prior ACKs received & *Socket healthy*
    while True:
        send_lock.acquire()
        if RTS and send_queue.qsize()>0:
            print("\nS", end='', flush=True)
            #print(str(send_queue.qsize()), end='', flush=True)
            message = send_queue.get()
            if type(message) == Command:  #Validate msg is well formed
                netconn.send(message)
                if message.command == "ACK":  #Ack'd a Server's command
                    print("A", end='', flush=True)
                elif message.command == "HBT":  #Ack'd a Server's command
                    print("H", end='', flush=True)
                elif message.command == "NAME":  #Ack'd a Server's command
                    print("N", end='', flush=True)
                else:
                    print("C", end='', flush=True)  #Sent a Client command
            else:  #Else abandon the bad outgoing message
                print("!", end='', flush=True)
            print(str(ack_queue.qsize()), end='', flush=True)
            print(str(recv_queue.qsize()), end='', flush=True)
            message = ""
            print("s", end='', flush=True)  #wrap it up
        send_lock.release()

def recv_loop():
    global netconn
    print("Client Receive Thread Started")
    while True:
        message = netconn.socket_recv()  #Get any inbound messages
        print("\nR", end='', flush=True)
        recv_lock.acquire()
        if type(message) == Command:  #Confirm whether msg is properly formed
            if message.command == "ACK": #send_queue will be waiting for  this
                ack_queue.put(message)
                print("A", end='', flush=True)
            else:
                recv_queue.put(message) #Then push onto the incoming queue
                print("C", end='', flush=True)
        else:  #Else abandon the bad incoming message
            print("!", end='', flush=True)
        print(str(ack_queue.qsize()), end='', flush=True)
        print(str(recv_queue.qsize()), end='', flush=True)
        message = ""
        recv_lock.release()

        #Now process recv_queue here
        proc_lock.acquire()
        if ack_queue.qsize()>0:
            pop_ack = ack_queue.get()
            if type(pop_ack) == Command:  #Validate msg is well formed
                #*** Insert code to process ACK messages ***
                pass
            else:
                print("!", end='', flush=True)
            pop_ack = ""
        if recv_queue.qsize()>0:
            pop_cmd = recv_queue.get()
            if type(pop_cmd) == Command:  #Validate msg is well formed
                #*** Insert code to process CMD messages ***
                #Probably a call to Gameplay passing the command to 
                pass
            else:
                print("!", end='', flush=True)
            pop_cmd = ""
        
        #wrap it up
        print("r", end='', flush=True)
        print(str(ack_queue.qsize()), end='', flush=True)
        print(str(recv_queue.qsize()), end='', flush=True)
        proc_lock.release()

def main():
    #Start thread to send and receive Socket messages
    recv_thread = threading.Thread(target=recv_loop, daemon=True).start() #args=(netconn,), 
    send_thread = threading.Thread(target=send_loop, daemon=True).start() #args=(netconn,), 

    print("Starting Client process")  #All Client processing happens within this loop
    while True:
        clock.tick(60) #Max 60 ticks per second - possibly not needed
        win.fill((0,0,0))
        game_events(netconn, p)
        game_update()
        game_draw()
        board.draw(win)
        pg.display.update()
        network_check(netconn, p)

def game_events(netconn, p) -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                print("BYE!", end='', flush=True)
                playing = False
                pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                #Just a test - press enter to update Player's name
                name_cmd = Command(p.id, "NAME", ("Test Name"))
                lock.acquire()
                send_queue.put(name_cmd) 
                lock.release()
        if event.type == pg.VIDEORESIZE:
            # There's some code to add back window content here.
            surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)

def game_update() -> None:
    now = pg.time.get_ticks()
    board.update()
    #p.update("place_units")  #temp used 'place_unit'

#Should this def be inside Main()?  Not sure of the source of this code...
#def redrawWindow(win):
#    win.fill((255,255,255))
#    p.draw(win)  #Why is this "p"???
#    pg.display.update()

def game_draw() -> None:
    board.draw(win)

def network_check(netconn, p) -> None:
    global t_end
    print(".", end='', flush=True)
    if time.time() >= t_end:
        hbt_cmd = Command(p.id, "HBT", "Ready to play")
        send_lock.acquire()
        send_queue.put(hbt_cmd)  #Or use the Send Queue to send the command...
        send_lock.release()
        t_end = time.time() + 5 #Pause 5 seconds until next heartbeat / This delay is blocking (bad)

main() 


