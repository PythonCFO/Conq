import socket, pickle

class Server_Socket:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        try:
            self.client.bind(self.addr)
            self.listen(5)
            print("Server is listening for socket connections from players")
            #The actual Connections happen later
            #Now is only establishing a listener 
        except:
            print("Server Socket creations has failed")
            pass

class New_Client_Connection:
    def __init__(self, conn):
        self.connection = conn
        #Where is Welcome to CONQ?

    #Server send data to a Client
    def client_send(self, data):
        try:
            sent = self.connection.send(pickle.dumps(data))
            if sent == 0:
                #I AM LANDING HERE IF A CLIENT BREAKS OFF CONNECTION!!
                #Need to handle this better
                raise RuntimeError("socket connection broken")
                #Instead, ^^ maybe gracefully disconnect the player.
        except socket.error as e:
            print(e)
            return ("\nE" + str(e))

    #Socket receive data from a Client
    def client_recv(self):
        try:
            data = self.connection.recv(2048)
            #Wait for inbound msg
            if data == b'':
                #I AM LANDING HERE IF A CLIENT BREAKS OFF CONNECTION!!
                #Need to handle this better
                print("Connection broken; Goodbye")
                return
                #raise RuntimeError("socket connection broken")
                #Instead, ^^ maybe gracefully disconnect the player.
            else:
                message = pickle.loads(data)
                return message
        except socket.error as e:
            #print(e)
            return ("\nE" + str(e))

