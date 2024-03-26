import pygame as pg
from network import Network
import time 
import threading
from player import Player
from gameplay import Command, Gameplay
import queue

pg.init()
clock = pg.time.Clock()
t_end = time.time() + 5

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
                    #Go run Andrew's function....
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
                #print(str(ack_queue.qsize()), end='', flush=True)
                #print(str(recv_queue.qsize()), end='', flush=True)
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
            pop_cmd = ack_queue.get()
            if type(pop_cmd) == Command:  #Validate msg is well formed
                #*** Insert code to process ACK messages ***
                pass
            else:
                print("!", end='', flush=True)
            pop_cmd = ""
        if recv_queue.qsize()>0:
            pop_cmd = recv_queue.get()
            if type(pop_cmd) == Command:  #Validate msg is well formed
                send_queue.put(Command(p.id, "ACK", "Command " + pop_cmd.command + " received"))
                #*** Additional processing of CMD messages & Gameplay ***
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

    print("Starting Client Main() Loop")  #All Client processing happens within this loop
    while True:
        clock.tick(60) #Max 60 ticks per second
        game_events()
        network_check(netconn, p)

def game_events() -> None:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                print("BYE!", end='', flush=True)
                playing = False
                pg.quit()

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
