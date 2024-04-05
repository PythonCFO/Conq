# TODO: Need much input validation if keep testing using input statements
#       Issues change fundamentally with GUI

# Game Engine design should enhance test_turn.py to explictly set up the game board for all players, then 
#   initiate the Turn process which ends in victory

import sys
from collections import Counter
import random
from config import classic_territories, region_bonus, cards

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
    def __init__(self, _player, _territories, _deck):
        self.player = _player
        self.territories = _territories
        self.deck = _deck

    def calc_reinforcements_from_territories(self):
        return max(int(sum(1 for k, v in self.territories.items() if v.owner == self.player)/3),3)
    
    def calc_reinforcements_from_regions(self):
        result =  0
        # iterate thru list of unique regions
        for region in list(set({v.region for k, v in territories.items()})):
            # if sum of player territories in region = sum of all territories in region => get bonus
            total_region = list({v1.name for k1,v1 in territories.items() if v1.region == region})
            player_region = list({v1.name for k1,v1 in territories.items() if v1.region == region and v1.owner == turn.player})
            if player_region == total_region:
                result += region_bonus[region]  # region_bonus loaded from config.py 
        return result

    def exchange_cards(self):
        result = 0
        # TODO: Add 2 army benefit if own card NOTE: some rules limit to max 2 armies per turn in
        player_cards = Counter([v.unit for k, v in self.deck.items() if v.owner == self.player]).most_common()
        number_cards = Counter([v.unit for k, v in self.deck.items() if v.owner == self.player]).total()
        number_wild_cards = Counter([v.unit for k, v in self.deck.items() if v.owner == self.player])['All']
        if number_cards >= 3:
            # test if 3 or more of one unit
            if player_cards[0][1] + number_wild_cards >= 3:
                result = 5 
            # test if one of each unit
            elif len(player_cards) >= 3:
                result = 5 
        return result
        
    def is_territory_owned(self, territory, player, normal=True):
        pass
        return
    
    def add_reinforcements_to_territory(self, territory, armies):
        pass
        return
    
    def confirm_defender(self, attacker, attacking_territory, defending_territory):
        pass
        return

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
        pass
        return

    def update_for_conquest(self, attacking_territory, attack_dice, defending_territory):
        pass
        return
    
    def is_victory(self):
        pass            
        return

    def get_card(self):
        remaining_cards = [k for k, v in self.deck.items() if v.owner == 'Deck']
        player_card = random.choice(remaining_cards)
        print(self.player + ' you earned the ' + player_card + ' card')
        deck[player_card].owner = self.player


class GameEngine:
    def __init__


def set_up_test_data():
    # Need mock armies data in territories
    for territory in turn.territories:
        # Assign random armies to each territory for set up (ultimately part of set up function/class)
        territories[territory].armies = random.randint(1, 5) 
        # Give Jay a region to test bonus function
        if territories[territory].name in ['Eastern Australia', 'Indonesia', 'New Guinea', 'Western Australia']:
            territories[territory].owner = 'Jay'
        # Create known owner/armies to test attack functions
        if territories[territory].name == 'Brazil':
            territories[territory].owner = 'Andrew'
            territories[territory].armies = 1
        elif territories[territory].name == 'Peru':
            territories[territory].owner = 'Jay'
            territories[territory].armies = 7
        print(territories[territory].name, territories[territory].owner, territories[territory].armies)
    #for card in ['New Guinea', 'Western Australia', 'South Africa', 'China']:  #test 3 of a unit
    for card in ['New Guinea', 'Western Australia', 'South Africa', 'Wild_1']:  #test 3 of a unit with wild
    #for card in ['Indonesia', 'New Guinea', 'Western Australia', 'South Africa']:  #test 1 of each unit
    #for card in ['New Guinea', 'Western Australia', 'South Africa']:
        deck[card].owner = 'Jay'



if __name__ == '__main__':
    
    # Instantiate game objects - players, territories, cards, turn
    players = []
    players.append(Player('Andrew'))
    players.append(Player('Jay'))

    territories = {}
    for t in classic_territories:       
        # classic_territories is list of lists [Region, Territory, [Adjacent Territories]] in config.py
        territory = Territory(t[1], t[0], t[2], random.choice(['Andrew', 'Jay']))
        territories[t[1]] = territory
       
    deck = {}
    for card in cards:
        # deck is list of lists [Territory, Unit]
        deck[card[0]] = Card(card[0], card[1])
    

    # Jay's turn
    turn = Turn('Jay', territories, deck)
    
    set_up_test_data()
      
    # 1. Calc Reinforcements
    reinforcements_territories = turn.calc_reinforcements_from_territories()
    reinforcements_regions = turn.calc_reinforcements_from_regions()
    reinforcements_cards = turn.exchange_cards()
    print(reinforcements_territories, reinforcements_regions, reinforcements_cards)
    reinforcements = reinforcements_territories + reinforcements_regions + reinforcements_cards
    print(turn.player + ", you have " + str(reinforcements) + " armies to place")
    
    # 2. Place reinforcements
    while reinforcements > 0:
        while True:
            territory_to_reinforce = input('What territory do you want to reinforce? ')
            #if turn.is_territory_owned(territory_to_reinforce, turn.player):
            if territories[territory_to_reinforce].owner == turn.player:
                break
            else:
                print("You do not own that territory. ")
        while True:
            armies_to_place = int(input("How many armies would you like to place? "))
            if armies_to_place <= reinforcements:
                reinforcements -= armies_to_place
                territories[territory_to_reinforce].armies += armies_to_place
                print('You have ' + str(reinforcements) + ' left to place. ')
                break
            else:
                print("You do not have that many reinforcements to place. ")
            
    print('Reinforcement Phase is complete ')
    
    # 3. Attack Phase
    print('Begin Attack phase')
    flag_earned_card = False
    while True:    #This get replaced in GUI with a button that says Make Attack or another that says Done Attack
        attack_decision = input("Do you want to make an attack (Y/N)? ")
        if attack_decision == 'N':
            break
        else:
            # determine attacking territory and defending territory
            while True:
                attack_from = input("From what country to you want to attack? ")
                #if turn.is_territory_owned(attack_from, turn.player):   #add test for more than 1 army
                if territories[attack_from].owner == turn.player:
                    while True:
                        defend_from = input("What country do you want to attack? ")
                        #if turn.confirm_defender(turn.player, attack_from, defend_from):
                        if (territories[defend_from].owner != turn.player and 
                            defend_from in territories[attack_from].adjacencies):
                            break
                        elif territories[defend_from].owner == turn.player:
                            print("You cannot attack yourself.  Pick another country to attack.")
                        elif not defend_from in territories[attack_from].adjacencies:
                            print(defend_from + " is not connected to " + attack_from)
                    break
                else:
                    print('You do not own that country.  You must attack from one of your countries.')
            print("You are attacking from " + attack_from + " to " + defend_from + ".")    
            # make attack
            while True: 
                attack_dice = int(input("How many dice would do you want to use to attack? "))
                #print(attacker, sum([territory.armies for territory in territories if territory.name == attacker]))
                
                if attack_dice > 0 and attack_dice <= min(3, territories[attack_from].armies):
                    break
                else:
                    print("That is not a valid number of dice.  Please select a number between 1 and 3 ")

            # Simple assumption of max defense until get gui connected
            defense_dice = min(2, territories[defend_from].armies)
            print("Attack from " + attack_from + " with " + str(attack_dice) + " dice to " 
                + defend_from + " defended with " + str(defense_dice) + " dice")
            attack_losses, defense_losses = turn.roll_attack(attack_dice, defense_dice)

        flag_conquest = False      # will need this when use functions for stuff below
        print('Attacker had ' + str(territories[attack_from].armies) + ' armies')
        territories[attack_from].armies -= attack_losses
        print('Attacker now has ' + str(territories[attack_from].armies) + ' armies')
        print('Defender had ' + str(territories[defend_from].armies) + ' armies')
        territories[defend_from].armies -= defense_losses
        print('Defender now has ' + str(territories[defend_from].armies) + ' armies')
        # check if conquered territory
        if territories[defend_from].armies == 0:
            flag_earned_card = True
            armies_to_move = int(input("How many armies would you like to move into " + defend_from 
                                    + " ?  You can must move at least " + str(attack_dice) + " and can move "
                                    + "as many as " + str(territories[attack_from].armies-1) + ". "))
            territories[attack_from].armies -= int(armies_to_move)
            territories[defend_from].armies += int(armies_to_move)
            territories[defend_from].owner = turn.player
            # check if won game
            player_territories = sum([1 for k, v in territories.items() if v.owner == turn.player])
            total_territories = len(territories)
            #print(turn.player + ' has ' + str(player_territories) + ' territories of a total of ' + str(total_territories) + ' territories')
            if sum([1 for k, v in territories.items() if v.owner == turn.player]) == len(territories):
                flag_victory = True
                print(turn.player + ' has won the game.')

    # 4. Troop Move Phase
    # Hack code to enfore loops until valid choices made.  GUI can simply not change state until error checking 
    #   complete and valid data input.  Use message box or bar to provide data warnings
    print('Begin troop move phase')
    while True:
        move_from = input("Select a country to move from.  If do not want a troop move, hit Enter. ")
        if len(move_from) == 0:
            break
        #elif turn.is_territory_owned(move_from, turn.player):  #TODO: Add testing for valid countries
        elif territories[move_from].owner == turn.player:
            while True: 
                move_to = input("Select a country to move to. ")
                #if turn.is_territory_owned(move_to, turn.player): 
                if territories[move_to].owner == turn.player:
                    while True:
                        armies_to_move = int(input('How many armies would you like to move? '))
                        if armies_to_move > territories[move_from].armies - 1:
                            print('You can move a maximum of ' + str(territories[move_from].armies - 1) + ' armies')
                        else:
                            break
                    territories[move_from].armies -= armies_to_move
                    territories[move_to].armies += armies_to_move
                    break
                else:
                    print("You do not own that territory.  Pick another. ")
        else:
            print('You do not own that territory.  Pick another. ')
            continue
        break
    
    # 5. Card Phase
    print('Begin card phase')
    if flag_earned_card:
        turn.get_card()

    # End of Turn
    print('Your turn is complete')        



    
    
