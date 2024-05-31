import config
from user import User
from game import Game, Command, Gamestate
from gamedb import ref

# These are functions to handle INCOMING COMMANDS from clients

def hbt(cmd):
    config.send_queues[cmd.userID].put(Command(cmd.userID, "ACK", "HBT received"))  #Add to the send queue

def ack(cmd):
    #Consider implementing a checklist, confirming that outbound commands are all ACK'd
    pass

def whoami(cmd):  # getting player setup initially (may not be needed)
    # Send current USER object to this user in response
    ref.child("logging").push(f"WHOAMI from {cmd.userID}; pushing WHOAMI, PLAYERS to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "WHOAMI", config.users[cmd.userID]))  #Add to the send queue
    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "PLAYERS", config.players))  #Add to the send queue

def join(cmd, mygame):  # player wants to join a game
    # Need to differentiate between 'users' and 'players'
    # User should be sending the desired gameID to the Server
    # Server replied with detailed GAME info
    # Then send the list of users[] to all other players

    ref.child("logging").push(f"JOIN from {cmd.userID}; pushing GAME to send_queue")  #Log the command
    mygame.add_player(cmd.userID)  #Append new player to game.players dict

    # p_json = {str(cmd.userID): mygame.players[cmd.userID]} 
    # ref.child("players/" + str(cmd.userID)).set(p_json)  #Append new player to RTDB

    config.send_queues[cmd.userID].put(Command(cmd.userID, "GAME", config.gameID))  #Send player the gameID
    
    p_json = {'name': mygame.players[cmd.userID]} 
    ref.child("players/" + str(cmd.userID)).set(p_json)  #Append new player to RTDB
    #ref.child("territories/" + str(t)).set(t_json) #send all Territories ^^ to RTDB

def profile(cmd, mygame):  # player wants to update their preferences
    # Update the user's profile preferences
    mygame.players[cmd.userID] = cmd.cmd_data  
    # Send updated player name to all players
    ref.child("logging").push(f"PROFILE from {cmd.userID}; pushing PLAYERS to send_queue")
    p_json = {'name': mygame.players[cmd.userID]} 
    ref.child("players/" + str(cmd.userID)).set(p_json)  #Append new player to RTDB
    for p in mygame.players.keys():
        config.send_queues[p].put(Command(cmd.userID, "PLAYERS", mygame.players))  #Add to the send queue

def game_all(cmd, mygame):
    # Client requests ALL game details - They can get this from RTDB now
    ref.child("logging").push(f"GAME from {cmd.userID}; pushing GAME {mygame} to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "GAME", mygame))  #Add to the send queue

def territory(cmd, mygame):
    # Client specifies 1 territory; response is the object for that 1 territory
    ref.child("logging").push(f"TERRITORY from {cmd.userID}; pushing {cmd.cmd_data}: {mygame.territories.get(cmd.cmd_data)} to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "TERRITORY", mygame.territories[cmd.cmd_data]))  #Add to the send queue

def take(cmd, mygame):
    # Test command to take ownership of a territory
    # Update territory info

    mygame.territories[cmd.cmd_data].owner = cmd.userID

    ref.child("logging").push(f"TAKE from {cmd.userID}; pushing {cmd.cmd_data}: {mygame.territories[cmd.cmd_data]} to send_queue")
    t_json = {'owner': cmd.userID} 
    ref.child("territories/" + str(cmd.cmd_data)).update(t_json)  #Update new territory owner in RTDB
    config.send_queues[cmd.userID].put(Command(cmd.userID, "TERRITORY", mygame.territories.get(cmd.cmd_data)))  #Add to the send queue

def territories(cmd, mygame):
    # Client requests territories they control; response is a list of territories
    my_territories = []
    for t in mygame.territories:
        if mygame.territories[t].owner == cmd.userID:
            my_territories.append(t)
    ref.child("logging").push(f"TERRITORIES from {cmd.userID}; pushing list of territories to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "TERRITORIES", my_territories))  #Add to the send queue

def adjacent(cmd, mygame):
    # Client requests adjacent territories; response is a list of territories
    ref.child("logging").push(f"TERRITORIES from {cmd.userID}; pushing list of adjacent territories to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "ADJACENT", mygame.territories[cmd.cmd_data].adjacencies))  #Add to the send queue

def cards(cmd):  # Player wants to play cards
    #TODO: Need to filter down to the cards held by this user
    # Verify that the cards submitted 1. are owned by user and 2. make up a set
    # Calculate the troop value of the cards - qty plus territory bonus
    # Issue armies to the user
    ref.child("logging").push(f"CARDS from {cmd.userID}; pushing CARDS, ARMIES to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "CARDS", config.cards[cmd.userID]))  #Add to the send queue
    config.send_queues[cmd.userID].put(Command(cmd.userID, "ARMIES", 10))  #Add to the send queue
    # for u in config.users.keys():
    #     config.send_queues[u].put(Command(cmd.userID, "PLAYERS", config.players))  #Add to the send queue

def place(cmd, mygame):
    territory = cmd.cmd_data[0]
    place_qty = cmd.cmd_data[1]
    ref.child("logging").push(f"PLACE from {cmd.userID}; pushing {territory}: {place_qty} to send_queue")
    new_armies = mygame.territories[cmd.cmd_data[0]].armies + int(cmd.cmd_data[1])
    mygame.territories[territory].armies = mygame.territories[territory].armies + int(place_qty)
    t_json = {'armies': new_armies} 
    ref.child("territories/" + str(cmd.cmd_data[0])).update(t_json)  #Update new territory owner in RTDB
    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue
    #config.send_queues[cmd.userID].put(Command(cmd.userID, "ARMIES", 10))  #Add to the send queue

def attack(cmd):
    # Confirm user owns source country and has enough armies
    # Confirm target country is otherwise owned and is adjacent
    # Roll dice, determine army decreases
    # If target defeated, then begin troop move process
    # Send territory updates to all users
    ref.child("logging").push(f"ATTACK from {cmd.userID}; TERRITORY(1:m) to send_queue") #Source
    config.send_queues[cmd.userID].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue
    config.send_queues[cmd.userID].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue

def move(cmd):
    #TODO: Will need a way to limit to one source and one destination / or req qty of troops in 1 move
    # Confirm user owns source country and has enough armies
    # Confirm user owns the target country
    # Confirm the uninterrupted route of adjacencies
    # Send territory updates to all users
    ref.child("logging").push(f"MOVE from {cmd.userID}; TERRITORY(1:m) to send_queue") #Source
    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue
        config.send_queues[u].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue

def next(cmd, _mygame):
    #TODO: Confirm user turn is active
    # Advance turn to the next phase
    print(f"Current turn = {_mygame.gamestate.turn} {_mygame.gamestate.stage}")
    # If phases are complete, advance turn to next player
    ref.child("logging").push(f"NEXT from {cmd.userID}; pushing TURN(1:m) to send_queue")
    #Complete this Stage of the Player's Turn
    _mygame.gamestate.next_stage()

    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "TURN", config.turn))  #Add to the send queue

