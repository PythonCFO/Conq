from config import classic_territories, region_bonus, classic_cards

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
            territories[t[1]] = territory
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
        self.deck = {}
        for c in classic_cards:
            self.deck[c[0]] = Card(c[0], c[1])

    def setup_territories(self):
        player_names = self.players.keys()
        #territory_names = list(self.territories.keys())
        #territory_names = list(t.name for t in self.territories.values() if t.owner=='Vacant')
        flag_assign_territories = True
        while flag_assign_territories:
            for p in player_names:
                #print(choice(list(t.name for t in self.territories.values() if t.owner=='Vacant')))
                #sys.exit()
                t = choice(list(t.name for t in self.territories.values() if t.owner=='Vacant'))
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
                t = choice(list(t.name for t in self.territories.values() if t.owner==p)) 
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

