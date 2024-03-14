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
root.geometry("1024x768+400+100")

label = ctk.CTkLabel(master=root, text="IP Address: ")
label.pack(padx=20, pady=20)

textbox = ctk.CTkTextbox(master=root, width=400, corner_radius=0)
textbox.pack(padx=20, pady=20)
textbox.insert("end", "X:X:X:X\n")

button = ctk.CTkButton(master=root, text="TestBtn")  #tabview.tab("tab 1"))
button.pack(padx=20, pady=20)


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

# Start up a thread dedicated to managing Socket connections
socket_thread = threading.Thread(target=socket_manager, daemon=True)                               
socket_thread.start()

#Start up the GUI thread to run the Risk server
root.mainloop() 

