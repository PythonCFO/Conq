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
            return pickle.loads(self.client.recv(2048))
        except:
            print("Connection failed")
            pass

    #Socket send data to Server
    def send(self, data):
        try:
            sent = self.client.send(pickle.dumps(data))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
            return str(e)

    #Socket receive data from Server
    def client_recv(self):
        bytes_recd = 0
        msg = self.sock.recv(2048)
        if msg == b'':
            raise RuntimeError("socket connection broken")
        bytes_recd = bytes_recd + len(msg)
        return b''.join(msg)

