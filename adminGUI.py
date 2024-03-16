import tkinter as tk
import customtkinter as ctk 
import threading
from _thread import *
import socket
from player import Player

'''  ToDo
    Use a better GUI widget to display comms traffic
    Improve the GUI layout
    New connections need to be stored in unique variables, or ** added to a collection
    GUI needs to display list of connected players
        Maybe this ^^ is using a TreeView for navigating to each of them?
    GUI needs to display status
    Create a collection of Players in a Game that can take turns
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

textbox.insert("end", "X:X:X:X\n")


def socket_manager():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 5555))
    s.listen(5)
    print("Server is listening for socket connections")
    while True:
        conn, address = s.accept()     # Blocks, waiting for connection
        new_player = Player(conn)
        all_players.append(new_player)
        print("New connection from {}".format( address ))
        #print("Active Players: " + str(len(all_players)))
        update_players()
        c = 0
        for p in all_players:
            print("Player " + str(c) + ": " + str(p.id))
            c += 1
        start_new_thread(threaded_client, (conn,))
        
def threaded_client(conn):  # Create a Thread for each new Client Socket Connection
    print("Inside threaded client")
    conn.send(str.encode("Client thread here"))
    reply = ''
    while True:
        try:
            data = conn.recv(2048)  #So if client does not respond to new connection, this server will disconnect.
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                print("Snd: Goodbye player " + str(conn))
                textbox.insert("end", "Snd: Goodbye player " + str(conn) + "\n")
                remove_player(conn)
                update_players()
                break  #Exit this While loop; closes the Socket for this specific Client
            else:
                print("Rcvd: " + reply + " : Snd: ACK")
                textbox.insert("end", "Rcvd: " + reply + " : Snd: ACK\n")
                conn.sendall(str.encode("ACK"))
        except:
            print("Exited at the Except statement")
            break

    print("Connection closed to " + str(conn))
    textbox.insert("end", "Connection closed to " + str(conn)+ "\n")
    conn.close()

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
        list_players.insert(index, "Player" + str(index) + " " + str(p.id) + ": " + str(p.name) + "\n")

# Start up a thread dedicated to managing Socket connections
socket_thread = threading.Thread(target=socket_manager, daemon=True)                               
socket_thread.start()

#Start up the GUI thread to run the Risk server
root.mainloop() 

