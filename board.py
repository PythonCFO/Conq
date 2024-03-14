class Board:
    def __init__(self):
        self.territories = []
        self.connections = []

    def add_territory(self, territory):
        self.territories.append(territory)

    def add_connection(self, territory1, territory2):
        self.connections.append((territory1, territory2))

class Territory:
    def __init__(self, name, owner, armies):
        self.name = name
        self.owner = owner
        self.armies = armies