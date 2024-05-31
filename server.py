import config
import socket
import threading
import pickle
import queue
import time
from user import User
from game import Game, Command, Gamestate
from server_threads import send_loop, recv_loop
from server_commands import *
#import server_commands
from gamedb import ref

#Server to clear out previous game activity from gamedb (debug)
ref.child("territories").delete()
ref.child("commands").delete()
ref.child("logging").delete()
ref.child("players").delete()

send_queue = queue.Queue()  # Each client has a dedicated queue for sending out comms
recv_queue = queue.Queue()  # Recv queue is shared by all clients
send_lock = threading.Lock()
recv_lock = threading.Lock()

def socket_mgr():
    global users, send_queue, recv_queue, ack_queue, send_queues, network_provisioned        
    #Listen/wait for Socket connections
    server = "localhost"
    port = 5556
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ref.child("logging").push("Binding Socket to server port.")
    while True:
        try:
            s.bind((server, port))
            network_provisioned = True
            break
        except socket.error as e:
            print(".", end='', flush=True)
            time.sleep(1)
    s.listen(5)
    ref.child("logging").push("Socket_mgr started - listening for connections")
    total_conns = 0
    while True:  
        conn, addr = s.accept()  #Blocking wait for user to connect via Socket
        ref.child("logging").push("Connecting...")
        total_conns += 1
        user = User()  #Server creates a user object

        config.users[user.userID] = user  #Add new user to the Dictionary
        config.users[user.userID].name = "Player_" + str(total_conns)  #Name the user
        config.users[user.userID].connected = True  #Enable comms with this user
        
        config.send_queues[user.userID] = queue.Queue() #Add new queue to send_queues Dictionary

        ref.child("logging").push("Starting send_loop and recv_loop threads for: " + user.name)
        recv_thread = threading.Thread(name=str(user.userID)+"_recv", target=recv_loop, args=(conn, user.userID, config.send_queues[user.userID], recv_queue), daemon=True).start()
        send_thread = threading.Thread(name=str(user.userID)+"_send", target=send_loop, args=(conn, user.userID, config.send_queues[user.userID], recv_queue), daemon=True).start()

        #Welcome the new user
        config.send_queues[user.userID].put(Command(user.userID, "ACK", "Welcome to Conq!"))
        config.send_queues[user.userID].put(Command(user.userID, "WHOAMI", user))  #Send "server created" User obj

        print(f"New user: {user.userID}")
        print("Active Users:")
        for u in config.users.keys():
            if config.users[u].connected == True:
                print(f"   {config.users[u].name} - {config.users[u].userID}") 
        print("Active Threads:")
        for t in threading.enumerate():
            print(f"   {t.name}")

def process_queues():
    global users, send_queues, recv_queue, network_provisioned
    proc_lock =  threading.Lock()
    ref.child("logging").push(f"Processing queues running {recv_queue.qsize()}")
    while True:
        proc_lock.acquire()
        #print(f"recv_queue length is now {recv_queue.qsize()}")
        if recv_queue.qsize()>0:
            ref.child("logging").push(f"Pulling command 1 of {recv_queue.qsize()} to process")
            pop_cmd = recv_queue.get()
            ref.child("commands").push({'userID': str(pop_cmd.userID), 'cmd': str(pop_cmd.command), 'data': str(pop_cmd.cmd_data)})
            if pop_cmd.command == "HBT":  hbt(pop_cmd)
            elif pop_cmd.command == "ACK": ack(pop_cmd) #Check-off the original Cmd was ACK'd
            elif pop_cmd.command == "JOIN": join(pop_cmd, mygame)
            elif pop_cmd.command == "PROFILE": profile(pop_cmd, mygame)
            elif pop_cmd.command == "GAME": game_all(pop_cmd, mygame)   # These are server initiated cmds
            elif pop_cmd.command == "TERRITORY": territory(pop_cmd, mygame)
            elif pop_cmd.command == "TAKE": take(pop_cmd, mygame)
            elif pop_cmd.command == "TERRITORIES": territories(pop_cmd, mygame)
            elif pop_cmd.command == "ADJACENT": adjacent(pop_cmd, mygame)
            elif pop_cmd.command == "CARDS": cards(pop_cmd)
            elif pop_cmd.command == "PLACE": place(pop_cmd, mygame)
            elif pop_cmd.command == "ATTACK": attack(pop_cmd)
            elif pop_cmd.command == "MOVE": move(pop_cmd)
            elif pop_cmd.command == "NEXT": next(pop_cmd, mygame)
            elif pop_cmd.command == "WHOAMI": whoami(pop_cmd)
            ref.child("logging").push(f"Unknown command {pop_cmd.command} received from {pop_cmd.userID}")
            pop_cmd = ""
        proc_lock.release()

def cli_loop():
    global users, send_queue, recv_queue, network_provisioned
    time.sleep(2)
    while True:
        # time.sleep(.5)
        #     for u in config.users.keys():
        #         print(f"Sending: user:{u} cmd:{get_cmd} cmd_data:{get_cmd_data}")
        #         config.send_queues[u].put(Command(config.users[u].userID, get_cmd, get_cmd_data))

        if network_provisioned:
            cli_line = input("Enter a test command: ")
            if cli_line:
                cli_list = cli_line.split()
                cli_cmd = cli_list[0]
                print(f"Command: {cli_cmd}")
                if len(cli_list) > 1: print(f"Argument: {cli_list[1]}")
                if cli_cmd  == "TURN": cli_cmd_data = "turn"
                elif cli_cmd  == "ARMIES": cli_cmd_data = "armies"
                elif cli_cmd  == "TURNCARD": cli_cmd_data = "cardID"
                elif cli_cmd  == "GAME": cli_cmd_data = "gameID"
                elif cli_cmd  == "WORLD": cli_cmd_data = "gameID"
                elif cli_cmd  == "TERRITORY": cli_cmd_data = "territoryID"
                elif cli_cmd == "PLAYERS": cli_cmd_data = "players list"
                if cli_cmd in ( "TURN", "ARMIES", "TURNCARD", "GAME", "WORLD", "TERRITORY") and cli_cmd_data != "NA":
                    for u in config.users.keys(): 
                        if config.users[u].connected:
                            send_queue.put(Command(config.users[u].userID, cli_cmd, cli_cmd_data))
                else:
                    print("Invalid entry")
            time.sleep(.5)  #Allow response to be displayed before new prompt

#Users can connect to Server without a Game existing
    #Allow users to create a game, see existing games, and join an existing game
#Create game
    #Spins up a gameID and all "Prepare" steps
    #Load reference data (Territories, Cards)
    #Accept Join requests (JOIN game)
    #Accept Start request (START game)
#For now...
mygame = Game()
#The following will load reference data if not yet populated.
for t in mygame.territories:
    t_json = {'region':  str(mygame.territories[t].region), 'adjacencies': mygame.territories[t].adjacencies, 'owner': 'Vacant', 'armies': '0'}
    ref.child("territories/" + str(t)).set(t_json) #send all Territories ^^ to RTDB
    # for c in game.cards:
    #     c_json = {'unit':  str(game.cards[c].unit), 'owner': 'Deck'}
    #     ref.child("cards/" + str(c)).set(c_json) 

#Start threads to handle Socket communications and process messages for this new GameID
network_provisioned = False
print("Starting SocketMgr and ProcessQueues threads")
socketmgr_thread = threading.Thread(name="SocketMgr", target=socket_mgr, args=(), daemon=True).start() 
process_thread = threading.Thread(name="ProcessQueues", target=process_queues, args=(), daemon=True).start() 
while not network_provisioned: pass
#Create a thread to handle manual entry user input at command line
ref.child("logging").push("Starting CLI Thread")  #Manually execute commands using command line input
cli_thread = threading.Thread(name="CLI", target=cli_loop, args=(), daemon=True).start() #args=(netconn,), 

print("Active Threads:")  #For debug...
for t in threading.enumerate():
    print(f"   {t.name}")

while True:
    #All gameplay activity is meant to be event based
    #Any Server triggered events should happen here
    if False:
        time.sleep(5)  
        print("Active Players:")
        num = 0
        for u in config.users.keys():
            if config.users[u].connected == True:
                print(f"   {config.users[u].name} - {config.users[u].userID}")
                num += 1
        if num == 0:
            print("   none")
        print("Active Threads:")
        for t in threading.enumerate():
            print(f"   {t.name}")
