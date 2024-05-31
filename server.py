import config
import threading
import queue
import time
from game import Game, Command, Gamestate
from server_threads import socket_mgr
from gameplay import process_queues
from server_commands import *
from gamedb import ref

# ref.child("territories").delete()
ref.child("commands").delete()
ref.child("logging").delete()
ref.child("players").delete()
# Load reference data if not yet populated
# for t in mygame.territories:
#     t_json = {'region':  str(mygame.territories[t].region), 'adjacencies': mygame.territories[t].adjacencies, 'owner': 'Vacant', 'armies': '0'}
#     ref.child("territories/" + str(t)).set(t_json) #send all Territories ^^ to RTDB
# for c in game.cards:
#     c_json = {'unit':  str(game.cards[c].unit), 'owner': 'Deck'}
#     ref.child("cards/" + str(c)).set(c_json) 

send_queues = {}
recv_queue = queue.Queue()  # Recv queue is shared by all clients

def cli_loop(users, mygame, send_queues):
    global recv_queue, network_provisioned
    time.sleep(2)
    while True:
        if True: #network_provisioned:
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
                    for p in mygame.players.keys(): 
                        if mygame.players[p].connected:
                            send_queues.put(Command(mygame.players[p].userID, cli_cmd, cli_cmd_data))
                else:
                    print("Invalid entry")
            time.sleep(.5)  #Allow response to be displayed before new prompt

users = {}  # Users active on the game server (not players)
mygame = Game()

#Start threads to handle Socket communications and process messages for this new GameID
network_provisioned = False
socketmgr_thread = threading.Thread(name="SocketMgr", target=socket_mgr, args=(users, send_queues, recv_queue), daemon=True).start() 
process_thread = threading.Thread(name="ProcessQueues", target=process_queues, args=(mygame, recv_queue, send_queues), daemon=True).start() 
while not network_provisioned: pass
ref.child("logging").push("Starting CLI Thread")  #Manually execute commands using command line input
cli_thread = threading.Thread(name="CLI", target=cli_loop, args=(users, mygame, send_queues), daemon=True).start() #args=(netconn,), 

print("Active Threads:")  #For debug...
for t in threading.enumerate():
    print(f"   {t.name}")

while True:  # Any Server triggered events should happen in this loop:
    pass
