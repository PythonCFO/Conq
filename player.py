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
        self.x = 100
        self.y = 100
        self.vel = 5
        self.width = 50
        self.height = 50
        self.rect = (self.x, self.y, self.width, self.height)
        self.color = "red"


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

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        #pass

    def move(self):
        keys = pygame.key.get_pressed()
        if keys == True:
            print(keys)

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

