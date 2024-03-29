import socket, pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected to " + str(self.addr))
            data =  pickle.loads(self.client.recv(2048))  #Wait for an ACK
            if data.command == "ACK":
                # One-time receipt of "Welcome to Conq!" from Server
                print(data.cmd_data) 
            else:
                print("Initial message was not ACK")
            return
        except:
            print("Connection failed")
            pass

    #Socket send data to Server
    def send(self, data):
        try:
            sent = self.client.send(pickle.dumps(data))
            if sent == b'':
                #I AM LANDING HERE IF A CLIENT BREAKS OFF CONNECTION!!
                #Need to handle this better
                raise RuntimeError("socket connection broken")
                #Instead, ^^ maybe gracefully disconnect the player.
        except socket.error as e:
            print(e)
            return ("\nE" + str(e))

    #Socket receive data from Server
    def socket_recv(self):
        try:
            data = self.client.recv(2048)   #Wait for inbound msg
            if data == b'':
                print("Connection broken; Goodbye")
                return
                #raise RuntimeError("socket connection broken")
            else:
                message = pickle.loads(data)
                return message
        except socket.error as e:
            #print(e)
            return ("\nE" + str(e))



