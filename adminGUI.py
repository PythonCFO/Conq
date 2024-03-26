import tkinter as tk
import customtkinter as ctk 
import threading
from _thread import *
import socket
from player import Player
from gameplay import Gameplay, Command
import queue
from network_server import Server_Socket, New_Client_Connection

global textbox
all_players = []

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title = "Risk - Server Admin Tool"
root.geometry("1024x768+400+100")

root.grid_columnconfigure((0,1,2), minsize=300, weight=1, uniform = 'a')
root.grid_rowconfigure((0), weight=1, uniform = 'a')
root.grid_rowconfigure((1), minsize=300, weight=6, uniform = 'a')
root.grid_rowconfigure((2), minsize=200, weight=4, uniform = 'a')

frame_title = ctk.CTkFrame(master=root)
frame_upper = ctk.CTkFrame(master=root)
frame_lower = ctk.CTkFrame(master=root)
frame_1 = ctk.CTkFrame(master=frame_upper, border_width=2)
frame_2 = ctk.CTkFrame(master=frame_upper, border_width=2)
frame_3 = ctk.CTkFrame(master=frame_upper, border_width=2)
label_title = ctk.CTkLabel(master=frame_title, text="Server Admin Tool", height=96, font=("Arial", 36))
label_1 = ctk.CTkLabel(master=frame_1, text="Players", font=("Arial", 16))
label_2 = ctk.CTkLabel(master=frame_2, text="Game Status", font=("Arial", 16))
label_3 = ctk.CTkLabel(master=frame_3, text="Game Controls", font=("Arial", 16))
textbox = ctk.CTkTextbox(master=frame_lower, border_width=2) 

frame_title.grid(row=0, column=0, columnspan=3, sticky="nesw")
frame_upper.grid(row=1, column=0, columnspan=3, sticky="nesw")
frame_lower.grid(row=2, column=0, columnspan=3, sticky="nesw")
frame_1.pack(anchor='center', side="left", fill="both", expand=True, padx=10, pady=10)

frame_2.pack(anchor='center', side="left", fill="both", expand=True, padx=10, pady=10)
frame_3.pack(anchor='center', side="left", fill="both", expand=True, padx=10, pady=10)
label_title.pack(side="left", fill="both", expand=True) 
label_1.pack(side="top", anchor='w', padx=15, pady=12)#, fill="both", expand=True)
label_2.pack(side="left", anchor='ne', padx=15, pady=12)#, fill="both", expand=True)
label_3.pack(side="left", anchor='ne', padx=15, pady=12)#, fill="both", expand=True)
textbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)

player_values=[]
list_players = tk.Listbox(frame_1, listvariable=player_values, height=10, background="#2E2E2F")
list_players.pack(side="top", padx=10, pady=10, expand=True, fill="both")

send_queue = queue.Queue()
recv_queue = queue.Queue()
ack_queue = queue.Queue()
admin_queue = queue.Queue()
lock=threading.Lock()
send_lock=threading.Lock()
recv_lock=threading.Lock()
proc_lock=threading.Lock()

def socket_manager():
    def send_loop(new_client_conn, player):
        print("Client Send Thread Started: " + player.id)  #All Client processing happens within this loop   
        RTS = True  #Ready To Send - Prior ACKs received & *Socket healthy*
        while True:
            send_lock.acquire()
            if RTS and send_queue.qsize()>0:
                print("\nS", end='', flush=True)
                #print(str(send_queue.qsize()), end='', flush=True)
                message = send_queue.get()
                if type(message) == Command:  #Validate msg is well formed

                    new_client_conn.client_send(message)

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

    def recv_loop(new_client_conn, player):
        print("Client Receive Thread Started: " + player.id)
        while True:
            message = new_client_conn.client_recv()  #Get any inbound messages
            print("\nR", end='', flush=True)
            recv_lock.acquire()
            if type(message) == Command:
                textbox.insert("end", message.command + " from " + message.id + ": " + message.cmd_data + "\n")
                if message.command == "HBT": #send_queue will be waiting for  this
                    recv_queue.put(message)
                    print("H", end='', flush=True)
                elif message.command == "ACK": #send_queue will be waiting for  this
                    ack_queue.put(message)
                    print("A", end='', flush=True)
                else:
                    recv_queue.put(message) #Then push onto the incoming queue
                    print("C", end='', flush=True)
            else: 
                print("!", end='', flush=True)
                print(f"Goodbye to {player.name}")
                textbox.insert("end", "Goodbye to player " + player.name + "\n")
                remove_player(player.conn) 
                update_players()  #Needs to broadcast the change to all Players
                #TODO Need to close the SOCKET and Turn off the client THREADs!
                break  #Exit this While True loop; 
                        #closes the Socket for this specific Client - where??                
            #Wrap it up
            print(str(ack_queue.qsize()), end='', flush=True)
            print(str(recv_queue.qsize()), end='', flush=True)
            message = ""
            recv_lock.release()

            #Process all queues here - random that it is in recv thread
            #Is this code tied to the incoming message receipt? 
            #Data in a queue feels 'pre-certified' as okay to process
            proc_lock.acquire()
            if ack_queue.qsize()>0:
                pop_cmd = ack_queue.get()
                if type(pop_cmd) == Command:  #Validate msg is well formed
                    #Unlikely anything needs to be sent
                    #Only confirm previously sent CMDs have been received
                    #Insert code to process ACK messages
                    pass
                else:
                    print("!", end='', flush=True)  #queues should be all clean data
                pop_cmd = ""
            if recv_queue.qsize()>0:
                pop_cmd = recv_queue.get()
                if type(pop_cmd) == Command:  #Validate msg is well formed
                    send_queue.put(Command(new_player.id, "ACK", "Command " + pop_cmd.command + " received"))  #Or use the Send Queue to send the command...
                    #*** Additional processing of CMD messages & Gameplay ***
                else:
                    print("!recv_q", end='', flush=True)
                pop_cmd = ""
            #wrap it up
            print("r", end='', flush=True)
            print(str(ack_queue.qsize()), end='', flush=True)
            print(str(recv_queue.qsize()), end='', flush=True)
            proc_lock.release()

    #Set up Server side Socket and set it to listen
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = "localhost"
    port = 5555
    addr = (server, port)
    try:
        sock.bind(addr)
        sock.listen(5)
        print("Server is listening on socket")
    except:
        print("Failed to establish Server Socket")

    #Allow Players to connect to the Server
    while True:
        conn, address = sock.accept()     # Blocks, waiting for connection
        #There are many conn instances per Server!
        new_client_connection = New_Client_Connection(conn)
        new_player = Player(new_client_connection)  #Create a player linked to the Socket conn
        all_players.append(new_player)   #Do I really want to add Server to this???
        print(f"New connection from player ID: {new_player.id}")
        
        #Start threads to send/receive messages to one specific Client
        recv_thread = threading.Thread(target=recv_loop, args=(new_client_connection, new_player,), daemon=True).start() #args=(netconn,), 
        send_thread = threading.Thread(target=send_loop, args=(new_client_connection, new_player,), daemon=True).start() #args=(netconn,), 

        #Send and ACK indicating "Welcome to Conq" to the new_player
        ack_cmd = Command(new_player.id, "ACK", "Welcome to Conq!")
        print(f"Welcome new player {new_player.id}")
        textbox.insert("end", ("Welcome new player " + new_player.id + "\n"))
        send_lock.acquire()
        send_queue.put(ack_cmd)  #Or use the Send Queue to send the command...
        send_lock.release()

        update_players()
        print("\nAll Players:")
        for p in all_players:
            print("   Player" + ": " + p.id + " " + p.name)

    #print(f"Connection closed to {player.conn}")
    #textbox.insert("end", ("Connection closed to " + str(player.id) + "\n"))
    #player.conn.close()

def remove_player(conn):
    #remove this player from the list of players
    for index, p in enumerate(all_players):
        if all_players[index].conn == conn:
             all_players.remove(p)

def update_players():
    #refresh the list of players in the GUI
    list_players.delete(0,"end")
    for index, p in enumerate(all_players):
        #print(index, p)
        list_players.insert(index, "Player " + str(p.id) + ": " + str(p.name) + "\n")

#Start game to handle gameplay commands
gp = Gameplay()
# Start up a thread dedicated to managing Socket connections
socket_thread = threading.Thread(target=socket_manager, daemon=True).start()
#Start up the GUI thread to run the Risk server
root.mainloop() 


 