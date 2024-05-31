from config import classic_territories, region_bonus, classic_cards, Phase, Turn, Stage
from enum import Enum
import random

# Define a universal comms command, for Client-Server interaction and processing
class Command:
    def __init__(self, userID, command, cmd_data):
        self.userID = userID  #player = target of cmd
        self.command = command  #command = an item from a command dictionary
        self.cmd_data = cmd_data  #cmd_data = [] a list of key:values required for the command to execute

# Define a game
class Game:
    def __init__(self):
        self.gameID = 'uuid'   #An ID for the game to allow multiple games in parallel
        self.state = 'Ready'
        self.territories = self.load_territories()
        self.cards = self.load_cards()
        self.players = {}
        self.gamestate = Gamestate()

    def start_game(self):
        self.players = self.setup_players()
        self.setup_territories()
        self.setup_initial_armies()
        self.state = 'Playing'

    def load_territories(self):
        # Returns dictionary of Territory objects
        # defaulting to classic countries TODO: need process to select a map
        territories = {}
        # classic_territories is list of lists [Region, Territory, [Adjacent Territories]] in config.py
        for t in classic_territories:    
            #Territory(self, _name, _region, _adjacencies, _owner, _armies=0):
            territory = Territory(t[1], t[0], t[2], 'Vacant', 0)
            #print(f"{t[1]} {territory}")
            territories[t[1]] = territory
        t=territories.get('Alaska')
        print(f"Name: {t.name}, Region: {t.region}, Adj: {t.adjacencies}, Owner: {t.owner}, Armies: {t.armies}")

        return territories

    def test_adj(self):
        # Purpose is to confirm all adjacencies are valid territories
        for t in self.territories:
            for a in self.territories[t].adjacencies:
                if a in self.territories:
                    print(t, a)
                else:
                    print("Error - ", a)

    def load_cards(self):
        deck = {}
        for c in classic_cards:
            deck[c[0]] = Card(c[0], c[1])
        return deck

    def add_player(self, uuid):
        if not uuid in self.players:
            self.players[uuid] = "Player" + str(len(self.players) + 1)
        # Need to update everyone on new list of Players

    def setup_territories(self):
        player_names = self.players.keys()
        #territory_names = list(self.territories.keys())
        #territory_names = list(t.name for t in self.territories.values() if t.owner=='Vacant')
        flag_assign_territories = True
        while flag_assign_territories:
            for p in player_names:
                #print(choice(list(t.name for t in self.territories.values() if t.owner=='Vacant')))
                #sys.exit()
                t = random.choice(list(t.name for t in self.territories.values() if t.owner=='Vacant'))
                self.territories[t].owner = p
                self.territories[t].changeColor(self.players[p].color)
                #self.territories[t].owner = self.players[p].color
                
                #print(self.territories[t].name, self.territories[t].owner, self.players[p].color, 
                #      len(list(t.name for t in self.territories.values() if t.owner=='Vacant')))
                if len(list(t.name for t in self.territories.values() if t.owner=='Vacant')) == 0:
                    flag_assign_territories = False
                    break
                #else:
                #    print(len(list(t.name for t in self.territories.values() if t.owner=='Vacant')))
        
    def setup_initial_armies(self):
        # Four player game has each player start with 30 armies
        for p in self.players.keys():
            armies = 30
            # Place two armies in each territory owned by player
            for t in [t.name for t in self.territories.values() if t.owner==p]:
                self.territories[t].armies = 2
                armies -= 2
            # Distribute remaining armies randomly across territories owned by player
            while armies > 0:
                t = random.choice(list(t.name for t in self.territories.values() if t.owner==p)) 
                self.territories[t].armies += 1
                armies -= 1
        
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

class Territory:
    def __init__(self, _name, _region, _adjacencies, _owner, _armies):
        self.name = _name
        self.region = _region
        self.adjacencies = _adjacencies
        self.owner = _owner
        self.armies = _armies

class Card:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
        self.owner = 'Deck'

class Gamestate:
    def __init__(self):
        self.phase = "Setup"   
        self.turn = ""
        self.stage = ""

    def start_play(self):
        # where to do all the things to get started?  Here or elsewhere??
        #Randomize the sequence of play? - use a Dict w/ (uuid and sequence#}
        self.phase = Phase("Play")
        self.turn = Turn(0)
        self.stage = Stage(0)

    def next_stage(self):
        self.stage = self.stage + 1  # Next stage of turn
        if self.stage == Stage.NP:
            self.next_player()

    def next_player(self):
        self.turn = self.turn + 1  # Next player
        if self.turn == Turn.NP:  
            self.turn = Turn(0)  # Start back with the first player again
        self.stage = Stage(0)  # Beginning stage of this player's turn

    def victory_check(self, territories):
        #Where to check if the last territory taken won the game for attacker??
        #Check ownership of all Territories.  If only 1 owner then game over!
        active_players = {}
        for t in territories:
            if not t.owner in active_players:
                active_players.append(t.owner)
        if len(active_players) == 1:
            print(f"Game over!")
            self.end_play()
        return active_players
    
    def end_play(self):
        self.phase = Phase.Done
        self.turn = Turn.NP
        self.stage = Stage.NP

