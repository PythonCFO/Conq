import uuid
import pygame

class Player:
    def __init__(self, conn):
        self.name = "TBD"
        self.id = uuid.uuid1()
        self.conn = conn
        self.conn_health = 0
        self.territories = []
        self.reinforcements = 0
        self.cards = []

    def deploy_armies(self, territory, armies):
        # Weak ChatGPT code...
        if territory in self.territories:
            territory.armies += armies

    def attack_territory(self, attacking_territory, defending_territory, armies):
        # Need to determine if Territoty knows "neighboring territies" or if a separate object "Connections" between Territories
        if attacking_territory in self.territories: # and (attacking_territory, defending_territory) in board.connections:
            # Implement attack logic
            pass

    def fortify_position(self, source_territory, target_territory, armies):
        if source_territory in self.territories and target_territory in self.territories:
            # Implement fortify logic
            pass  

    def update(self, phase: str) -> None:
        if phase == "place_units":
            pass #self.place_units()
        elif phase == "move_units":
            pass #self.move_units()
        elif phase == "attack_country":
            pass #self.attack_country()

