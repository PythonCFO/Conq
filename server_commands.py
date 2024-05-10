import config
from user import User
from game import Game, Command

def hbt(cmd):
    config.send_queues[cmd.userID].put(Command(cmd.userID, "ACK", "HBT received"))  #Add to the send queue

def ack(cmd):
    #Consider implementing a checklist, confirming that outbound commands are all ACK'd
    pass

def whoami(cmd):  # player wants to update their preferences
    # Send current USER object to this user in response
    if config.VERBOSE: print(f"WHOAMI from {cmd.userID}; pushing WHOAMI, PLAYERS to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "WHOAMI", config.users[cmd.userID]))  #Add to the send queue
    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "PLAYERS", config.players))  #Add to the send queue

def join(cmd):  # player wants to join a game
    # New users are automatically added to users.  
    # In future, should differentiate between 'users' and 'players'
    # Send GAME info (including game UUID) to the new user
    # Send list of users[] to all other players
    if config.VERBOSE: print(f"JOIN from {cmd.userID}; pushing GAME to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "GAME", config.gameID))  #Add to the send queue

def profile(cmd):  # player wants to update their preferences
    # Update the user's profile preferences
    config.users[cmd.userID] = cmd.cmd_data  #NOT SAFE! - Trusts the user provided object
    # Send updated USER object to player
    # Send updated user name to all players
    if config.VERBOSE: print(f"PROFILE from {cmd.userID}; pushing WHOAMI, PLAYERS to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "WHOAMI", cmd.cmd_data))  #Add to the send queue
    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "PLAYERS", config.players))  #Add to the send queue

def game(cmd):
    if config.VERBOSE: print(f"GAME from {cmd.userID}; pushing GAME to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "GAME", config.gameID))  #Add to the send queue

def world(cmd):
    #Presumably this requests ALL details of the gameboard and play?
    if config.VERBOSE: print(f"WORLD from {cmd.userID}; pushing WORLD to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "WORLD", config.world))  #Add to the send queue

def territory(cmd):
    if config.VERBOSE: print(f"TERRITORY from {cmd.userID}; pushing TERRITORY to send_queue")
    #TODO: cmd to specify 1 territory; response is data for that 1 territory
    config.send_queues[cmd.userID].put(Command(cmd.userID, "TERRITORY", config.territory))  #Add to the send queue

def cards(cmd):  # Player wants to play cards
    #TODO: Need to filter down to the cards held by this user
    # Verify that the cards submitted 1. are owned by user and 2. make up a set
    # Calculate the troop value of the cards - qty plus territory bonus
    # Issue armies to the user
    if config.VERBOSE: print(f"CARDS from {cmd.userID}; pushing CARDS, ARMIES to send_queue")
    config.send_queues[cmd.userID].put(Command(cmd.userID, "CARDS", config.cards[cmd.userID]))  #Add to the send queue
    config.send_queues[cmd.userID].put(Command(cmd.userID, "ARMIES", 10))  #Add to the send queue
    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "PLAYERS", config.players))  #Add to the send queue

def place(cmd):
    # Confirm user has armies to be placed
    # Add 1 army to the specified territory
    # Decrement armies available to place
    # Send updated armies count to user
    # Send modified territory to all
    if config.VERBOSE: print(f"PLACE from {cmd.userID}; TERRITORY(1:m), ARMIES to send_queue")
    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue
    config.send_queues[cmd.userID].put(Command(cmd.userID, "ARMIES", 10))  #Add to the send queue

def attack(cmd):
    # Confirm user owns source country and has enough armies
    # Confirm target country is otherwise owned and is adjacent
    # Roll dice, determine army decreases
    # If target defeated, then begin troop move process
    # Send territory updates to all users
    if config.VERBOSE: print(f"ATTACK from {cmd.userID}; TERRITORY(1:m) to send_queue") #Source
    config.send_queues[cmd.userID].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue
    config.send_queues[cmd.userID].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue

def move(cmd):
    #TODO: Will need a way to limit to one source and one destination / or req qty of troops in 1 move
    # Confirm user owns source country and has enough armies
    # Confirm user owns the target country
    # Confirm the uninterrupted route of adjacencies
    # Send territory updates to all users
    if config.VERBOSE: print(f"MOVE from {cmd.userID}; TERRITORY(1:m) to send_queue") #Source
    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue
        config.send_queues[u].put(Command(cmd.userID, "TERRITORY", territory))  #Add to the send queue

def next(cmd):
    # Confirm user turn is active
    # Advance turn to the next phase
    # If phases are complete, advance turn to next player
    if config.VERBOSE: print(f"NEXT from {cmd.userID}; pushing TURN(1:m) to send_queue")
    for u in config.users.keys():
        config.send_queues[u].put(Command(cmd.userID, "TURN", config.turn))  #Add to the send queue

