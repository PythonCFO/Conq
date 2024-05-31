from gamedb import ref
import threading
from server_commands import hbt, ack, join, profile, game_all, territory, take, territories, adjacent, cards, place, attack, move, next, whoami

# Define a universal comms command, for Client-Server interaction and processing
class Command:
    def __init__(self, userID, command, cmd_data):
        self.userID = userID  #player = target of cmd
        self.command = command  #command = an item from a command dictionary
        self.cmd_data = cmd_data  #cmd_data = [] a list of key:values required for the command to execute

def process_queues(mygame, recv_queue, send_queues):
    #global users, recv_queue, network_provisioned
    proc_lock =  threading.Lock()
    ref.child("logging").push(f"Processing queues running {recv_queue.qsize()}")
    while True:
        proc_lock.acquire()
        #print(f"recv_queue length is now {recv_queue.qsize()}")
        if recv_queue.qsize()>0:
            ref.child("logging").push(f"Pulling command 1 of {recv_queue.qsize()} to process")
            pop_cmd = recv_queue.get()
            ref.child("commands").push({'userID': str(pop_cmd.userID), 'cmd': str(pop_cmd.command), 'data': str(pop_cmd.cmd_data)})
            if pop_cmd.command == "HBT":  hbt(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "ACK": ack(pop_cmd, mygame, send_queues) #Check-off the original Cmd was ACK'd
            elif pop_cmd.command == "JOIN": join(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "PROFILE": profile(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "GAME": game_all(pop_cmd, mygame, send_queues)   # These are server initiated cmds
            elif pop_cmd.command == "TERRITORY": territory(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "TAKE": take(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "TERRITORIES": territories(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "ADJACENT": adjacent(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "CARDS": cards(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "PLACE": place(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "ATTACK": attack(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "MOVE": move(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "NEXT": next(pop_cmd, mygame, send_queues)
            elif pop_cmd.command == "WHOAMI": whoami(pop_cmd, mygame, send_queues)
            ref.child("logging").push(f"Unknown command {pop_cmd.command} received from {pop_cmd.userID}")
            pop_cmd = ""
        proc_lock.release()

class Gameplay:
    def __init__(self):
        self.cmd_queue = []  # queue Client commands as received to sequence execution
        # Ideally client Sockets receiving a command msg, invokes a METHOD on the Gameplay Object
        # This queue may need to be passed to Socket Threads to store RECV'd Commands

