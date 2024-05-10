import client_config
from network import Network, network_check
from game import Command
from user import User
from client_threads import send_loop, recv_loop
import time 
import threading
import queue
from client_commands import *

version = "0.1"
DEBUG = False
HBT = False

send_queue = queue.Queue()
recv_queue = queue.Queue()
send_lock=threading.Lock()
recv_lock=threading.Lock()
proc_lock=threading.Lock()

client_config.user = User()  #Generic user locally, ot be replaced by Server
playing = False  #Server has accepted User to play (Needs implementing)

def main():
    print(f"Starting GameFrame Client v{version}")
    run = True
    time.sleep(0.02)

    #Establish Server Socket connection
    client_config.user = User()
    n = Network() # Establish connection to Server

    #Start thread to send and receive Socket messages
    recv_thread = threading.Thread(target=recv_loop, args=(n, send_queue, recv_queue), daemon=True).start() #args=(netconn,), 
    send_thread = threading.Thread(target=send_loop, args=(n, send_queue, recv_queue), daemon=True).start() #args=(netconn,), 
    
    #Create a thread to handle manual entry user input at command line
    while not client_config.user.connected: pass
    cli_thread = threading.Thread(target=cli_loop, args=(), daemon=True).start() #args=(netconn,), 

    game = Game()

    HBT_time = time.time() + 5
    while True:
        time.sleep(.02)

        #game_events()
        process_queues(game)
        HBT_time = network_check(client_config.user.userID, HBT_time)
        try:
            pass
        except:
            run = False   #TODO Always 'run' but sometimes 'play' but bever bail out completely.
            print("Unknown Exception in main()!?")
            break

        #Execute various gameplay activities here
        #Refresh the gameplay GUI as needed

def network_check(userID, HBT_time):
    global send_lock, send_queue
    if time.time() >= HBT_time:
        if HBT:
            hbt_cmd = Command(userID, "HBT", "Ready to play")
            send_lock.acquire()
            send_queue.put(hbt_cmd)  #Or use the Send Queue to send the command...
            send_lock.release()
        return time.time() + 5
    else:
        return HBT_time       

def process_queues(game):
        global user, playing
        proc_lock.acquire()
        if recv_queue.qsize()>0:
            pop_cmd = recv_queue.get()
            print(f"     Pulling {pop_cmd.command} from queue of {recv_queue.qsize()+1} to process")
            if pop_cmd.command != "ACK": send_queue.put(Command(pop_cmd.userID, "ACK", "Command " + pop_cmd.command + " received"))
            if pop_cmd.command == "ACK":  ack(pop_cmd)
            elif pop_cmd.command == "WHOAMI": whoami(pop_cmd)  # When joining, Server sends this!
            elif pop_cmd.command == "JOIN": join(pop_cmd, game)
            elif pop_cmd.command == "GAME": gm(pop_cmd, game)
            elif pop_cmd.command == "WORLD": world(pop_cmd, game)
            elif pop_cmd.command == "TERRITORY": territory(pop_cmd)
            elif pop_cmd.command == "PLAYERS": players(pop_cmd)
            elif pop_cmd.command == "ARMIES": armies(pop_cmd)
            elif pop_cmd.command == "TURN": turn(pop_cmd)
            else:
                print("!!", end='', flush=True)
                print("")
            pop_cmd = ""
        proc_lock.release()

def cli_loop():
    global user, send_queue, network_connected

    print("Client cli_loop Thread started")  #Manually send commands using command line input
    time.sleep(2)
    while True:
        if client_config.user.connected:
            cli_cmd = input("Enter a test command: ")
            if cli_cmd  == "JOIN": cli_cmd_data = client_config.user
            elif cli_cmd == "PROFILE": cli_cmd_data = client_config.user
            elif cli_cmd  == "GAME": cli_cmd_data = "gameID"
            elif cli_cmd  == "WORLD": cli_cmd_data = "gameID"
            elif cli_cmd  == "TERRITORY": cli_cmd_data = "territoryID"
            elif cli_cmd  == "CARDS": cli_cmd_data = ("cardID_1", "cardID_2", "cardID_3")
            elif cli_cmd  == "PLACE": cli_cmd_data = "territoryID"
            elif cli_cmd  == "ATTACK": cli_cmd_data = ("territoryID_1", "territoryID_2")
            elif cli_cmd  == "MOVE": cli_cmd_data = ("territoryID_1", "territoryID_2")
            elif cli_cmd  == "NEXT": cli_cmd_data = "gameID"
            if cli_cmd in ("JOIN", "PROFILE", "GAME", "WORLD", "TERRITORY", "CARDS", "PLACE", "ATTACK", "MOVE", "NEXT"):
                send_queue.put(Command(client_config.user.userID, cli_cmd, cli_cmd_data))
            else:
                print("Invalid entry")
            time.sleep(.5)  #Allow response to be displayed before new prompt

class Game:
    def __init__(self):
        self.gameID = 'uuid'   #An ID for the game to allow multiple games in parallel
        self.state = 'Ready'
        self.territories = {}

main()
