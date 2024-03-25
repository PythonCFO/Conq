import tkinter as tk
import customtkinter as ctk 
import threading
from _thread import *
import socket, pickle
from player import Player
from gameplay import Gameplay, Command

'''  ToDo
    GUI needs to display game status
    Server needs to manage turns
    Server needs critical data objects
    Server needs defined command protocol with Clients
'''

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


def socket_manager():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 5555))
    s.listen(5)
    print("Server is listening for socket connections")
    while True:
        conn, address = s.accept()     # Blocks, waiting for connection
        new_player = Player(conn)
        all_players.append(new_player)
        print(f"New connection from player ID: {new_player.id}")
        update_players()
        print("All Players:")
        for p in all_players:
            print("   Player" + ": " + p.id + " " + p.name)


        #TODO  How is the following actually starting a new thread.  
        #No Start command??   
        #Looks like calling function in same process!!??
        
        #start_new_thread(threaded_client, (new_player,)).start
        
        client_socket_thread = threading.Thread(target=threaded_client, args=(new_player,), daemon=True)                               
        client_socket_thread.start()


#TODO -- For thread to send commands, it needs *Player* not just Conn
def threaded_client(player):  # Create a Thread for each new Client Socket Connection
    print("Inside threaded client")
    connection = player.conn
    hello_cmd = Command(player.id, "ACK", "Welcomes to Conq!")
    connection.send(pickle.dumps(hello_cmd))
    print("A new player has been welcomed to Conq!")
    while True:
        try:
            #All I am doing is awaiting receipt of messages, not sending
            client_cmd = pickle.loads(player.conn.recv(2048)) # Wait to receive Client data
            if client_cmd == "":  
                print("inside failure response section: 'if not data'")
                #Should be a Command.  Should be in a Network module.
                player.conn.send(pickle.dumps("Goodbye"))
                print(f"Snd: Goodbye {player.name}")
                textbox.insert("end", "Snd: Goodbye {player.name}\n")
                remove_player(player.conn) 
                update_players()
                break  #Exit this While loop; closes the Socket for this specific Client
            else:
                print(f"{client_cmd.command} from {client_cmd.id}: '{client_cmd.cmd_data}'")
                textbox.insert("end", client_cmd.command + " from " + client_cmd.id + ": " + client_cmd.cmd_data + "\n")
                player.conn.send(pickle.dumps(Command(player.id, "ACK", "Let's get to it!")))
        except:
            print("Exited at the Except statement")
            break

    print(f"Connection closed to {player.conn}")
    textbox.insert("end", ("Connection closed to " + str(player.id) + "\n"))
    player.conn.close()

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
socket_thread = threading.Thread(target=socket_manager, daemon=True)                               
socket_thread.start()

#Start up the GUI thread to run the Risk server
root.mainloop() 


