import uuid
from game import Command 

class User:
    def __init__(self):
        self.userID = str(uuid.uuid1())[:8]
        self.name = "TEMP"
        self.connected = False

