import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"  # This holds Server generated Client IDs

def threaded_client(conn):  # Create a Thread for each new Client Socket Connection
    global currentId
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)  #So if client does not respond to new connection, this server will disconnect.
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                print("Snd: Goodbye")
                break  #Exit this While loop; closes the Socket for this specific Client
            else:
                print("Rcvd: " + reply + " : Snd: ACK")
                conn.sendall(str.encode("ACK"))
        except:
            print("Exited at the Except statement")
            break

    print("Client connection closed.")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))