
# TODO: make decision re how GUI updates work.  Does game do a full screen refresh periodically (check all 
#       values) or does each change have the responsibility to cause affected area to be refreshed (e.g. 
#       conquer a territory leads to color change)


import sys
from collections import Counter
import random
from config import classic_territories, region_bonus, deck

class Player:
    def __init__(self, name):
        self.name = name

class Territory:
    def __init__(self, name, region, adjacencies, owner):
        self.name = name
        self.region = region
        self.adjacencies = adjacencies
        self.owner = owner
        self.armies = 0

class Card:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
        self.owner = 'Deck'

class Turn:
    def __init__(self, _player, _territories, _cards):
        self.player = _player
        self.territories = _territories
        self.cards = _cards

    def calc_reinforcements_from_territories(self):
        #Need to decide how track player object - player.name or player.id
        #armies_from_territories = max(int(sum(t.owner == self.player for t in self.territories)/3),3)
        return max(int(sum(1 for t in self.territories if t.owner == self.player)/3),3)
    
    def calc_reinforcements_from_regions(self):
        result =  0
        for region in list(set([t.region for t in territories])):
            if sum([1 for t in self.territories if t.region == region]) == sum([1 for t in self.territories if t.region == region and t.owner == self.player]):
                result += region_bonus[region]
        return result

    def exchange_cards(self):
        # TODO: Add 2 army benefit if own card
        player_cards =dict(Counter([c.unit for c in cards if c.owner == self.player]))
        if len([k for k, v in player_cards.items() if v > 2]) > 0 or len(player_cards) == 3:
            # TODO: implement card exchange variations
            result = 5 
        else:
            result = 0
        return result
        
    def is_territory_owned(self, territory, player, normal=True):
        for t in self.territories:
            if t.name == territory and (t.owner == player) == normal:  #Allows check of is player or is not player
                return True
        return False
    
    def add_reinforcements_to_territory(self, territory, armies):
        for t in self.territories:
            if t.name == territory:
                t.armies += armies

    def confirm_defender(self, attacker, attacking_territory, defending_territory):
        if self.is_territory_owned(defending_territory, attacker):
            print('You cannot attack yourself')
            return False
        else:
            for t in self.territories:
                if t.name == attacking_territory and defending_territory in t.adjacencies:
                    return True
        print(attacking_territory + ' and ' + defending_territory + ' are not connected.')
        return False    

    def roll_attack(self, att_dice, def_dice):
        # assume six-sided dice
        attack = random.choices(range(1,7), k=att_dice)
        attack.sort(reverse=True)
        defense = random.choices(range(1,7), k=def_dice)
        defense.sort(reverse=True)
        #print(attack, defense)
        attack_losses = 0
        defense_losses = 0
        for i in range(min(att_dice, def_dice)):
            if attack[i] > defense[i]:
                defense_losses += 1
            else:
                attack_losses += 1
        print('Attacker lost ' + str(attack_losses) + ' and Defender lost ' + str(defense_losses))
        return attack_losses, defense_losses

    def update_territories_for_battle(self, attacking_territory, attack_losses, defending_territory, defense_losses):
        # for GUI could change everything to setters which would include screen refresh
        flag_conquest = False
        for t in self.territories:
            if t.name == attacking_territory:
                print('Attacker had ' + str(t.armies) + ' armies')
                t.armies -= attack_losses
                #print('attack', type(attack_losses), type(defense_losses))
                print('Attacker now has ' + str(t.armies) + ' armies')
            elif t.name == defending_territory:
                print('Defender had ' + str(t.armies) + ' armies')
                t.armies -= defense_losses
                #print('defend', type(attack_losses), type(defense_losses))
                print('Defender now has ' + str(t.armies) + ' armies')
                if t.armies == 0:
                    #t.owner = self.player
                    flag_conquest = True        
        return flag_conquest

    def update_for_conquest(self, attacking_territory, attack_dice, defending_territory):
        for t in self.territories:
            if t.name == attacking_territory:
                armies_to_move = int(input("How many armies would you like to move into " + defending_territory 
                                       + " ?  You can must move at least " + str(attack_dice) + " and can move "
                                       + "as many as " + str(t.armies-1) + ". "))
                t.armies -=  armies_to_move
                break
        for t in self.territories:
            if t.name == defending_territory:
                t.owner = self.player
                t.armies = armies_to_move
    
    def is_victory(self):
        owned_countries =dict(Counter([t.owner for t in territories if t.owner == self.player]))
        if owned_countries == len(territories):
            return True
        else:
            return False

    def get_card(self):
        remaining_cards = []
        print(self.cards)
        #sys.exit()
        for c in self.cards:
            if c.owner == 'Deck':
                remaining_cards.append(c.name)
        print(remaining_cards)
        player_card = random.choice(remaining_cards)
        print(player_card)
        for c in self.cards:
            if c.name == player_card:
                c.owner = self.player
         
if __name__ == '__main__':
    # Mock up data
    players = []
    players.append(Player('Andrew'))
    players.append(Player('Jay'))

    territories = []
    #dict_ter = {}  # Added test example of making dict of objects for easier access to specific object
    for t in classic_territories:
        #territories.append(Territory(t[1], t[0], t[2], random.choice(['Andrew', 'Jay']))) # Randomly assign ownership
        temp_t = Territory(t[1], t[0], t[2], random.choice(['Andrew', 'Jay']))
        print(temp_t.name, temp_t.owner)
        territories.append(temp_t)
        #dict_ter[t[1]] = temp_t 
    
    ''' Test using dict of objects
    print(dict_ter['Siam'].owner)
    if dict_ter['Siam'].owner =='Jay':
        dict_ter['Siam'].owner = 'Andrew'
    else:
        dict_ter['Siam'].owner = 'Jay'
    print(dict_ter['Siam'].owner)
    '''


    cards = []
    for card in deck:
        cards.append(Card(card[0], card[1]))


    #for card in cards:
    #    if card.name in ['Peru', 'Brazil', 'Alaska', 'Iceland', 'Irkutsk']:
    #        card.owner = 'Jay'

    # Jay's turn
    turn = Turn('Jay', territories, cards)
    

    # Need mock armies data in territories
    for territory in turn.territories:
        territory.armies = random.randint(1, 5) 
        print(territory.name, territory.armies)
    
    
    # 1. Calc Reinforcements
    # mock data
    for t in turn.territories:
        if t.name == 'Brazil':
            t.owner = 'Andrew'
            t.armies = 1
        elif t.name == 'Peru':
            t.owner = 'Jay'
            t.armies = 7

    reinforcements_territories = turn.calc_reinforcements_from_territories()
    reinforcements_regions = turn.calc_reinforcements_from_regions()
    reinforcements_cards = turn.exchange_cards()
    #print(reinforcements_territories, reinforcements_regions, reinforcements_cards)
    reinforcements = reinforcements_territories + reinforcements_regions + reinforcements_cards
    print(turn.player + ", you have " + str(reinforcements) + " armies to place")
    
    # 2. Place reinforcements
    while reinforcements > 0:
        while True:
            territory_to_reinforce = input('What territory do you want to reinforce? ')
            if turn.is_territory_owned(territory_to_reinforce, turn.player):
                break
            else:
                print("You do not own that territory. ")
        while True:
            armies_to_place = int(input("How many armies would you like to place? "))
            if armies_to_place <= reinforcements:
                reinforcements -= armies_to_place
                turn.add_reinforcements_to_territory(territory_to_reinforce, armies_to_place)
                print('You have ' + str(reinforcements) + ' left to place. ')
                break
            else:
                print("You do not have that many reinforcements to place. ")
            
    print('Reinforcement Phase is complete ')
        
    # 3. Make Attacks

    print('Begin Attack phase')
    flag_earned_card = False
    while True:    #This get replaced in GUI with a button that says Make Attack or another that says Done Attack
        attack_decision = input("Do you want to make an attack (Y/N)? ")
        if attack_decision == 'N':
            break
        else:
            while True:
                attack_from = input("From what country to you want to attack? ")
                if turn.is_territory_owned(attack_from, turn.player):   #add test for more than 1 army
                    while True:
                        defend_from = input("What country do you want to attack? ")
                        if turn.confirm_defender(turn.player, attack_from, defend_from):
                            break
                    break
                else:
                    print('You do not own that country.  You must attack from one of your countries.')
            print("You are attacking from " + attack_from + " to " + defend_from + ".")    

            while True: 
                attack_dice = int(input("How many dice would do you want to use to attack? "))
                #print(attacker, sum([territory.armies for territory in territories if territory.name == attacker]))
                if attack_dice > 0 and attack_dice <= min(3, sum([territory.armies for territory in territories if 
                                                                territory.name == attack_from])-1):
                    break
                else:
                    print("That is not a valid number of dice.  Please select a number between 1 and 3 ")
            
            # Simple assumption of max defense until get gui connected
            defense_dice = min(2, sum([territory.armies for territory in territories if territory.name == defend_from]))
            print("Attack from " + attack_from + " with " + str(attack_dice) + " dice to " 
                + defend_from + " defended with " + str(defense_dice) + " dice")

            attack_losses, defense_losses = turn.roll_attack(attack_dice, defense_dice)
            flag_victory = turn.update_territories_for_battle(attack_from, attack_losses, defend_from, defense_losses)
            if flag_victory: 
                flag_earned_card = True
                turn.update_for_conquest(attack_from, attack_dice, defend_from)
            
    # Troop Move Phase
    # Hack code to enfore loops until valid choices made.  GUI can simply not change state until error checking 
    #   complete and valid data input.  Use message box or bar to provide data warnings
    print('Begin troop move phase')
    while True:
        move_from = input("Select a country to move from.  If do not want a troop move, hit Enter. ")
        if len(move_from) == 0:
            break
        elif turn.is_territory_owned(move_from, turn.player):  # Add testing for valid countries
            while True: 
                move_to = input("Select a country to move to. ")
                if turn.is_territory_owned(move_to, turn.player): 
                    armies_to_move = int(input('How many armies would you like to move? '))
                    # put code here to force discussion of place way and location to do this
                    for t in territories:
                        if t.name == move_from:
                            t.armies -= armies_to_move
                        elif t.name == move_to:
                            t.armies += armies_to_move
                    break
                else:
                    print("You do not own that territory.  Pick another. ")
        else:
            print('You do not own that territory.  Pick another. ')
            continue
        break

    # Get card if earned
    print('Begin card phase')
    if flag_earned_card:
        turn.get_card()

    # End of Turn
    print('Your turn is complete')        



    
    
