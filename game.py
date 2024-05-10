# Define a universal gameplay command, as a single object of class Command
class Command:
    def __init__(self, userID, command, cmd_data):
        self.userID = userID  #player = target of cmd
        self.command = command  #command = an item from a command dictionary
        self.cmd_data = cmd_data  #cmd_data = [] a list of key:values required for the command to execute

# Define a game
class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id   #An ID for the game to allow multiple games in parallel
        self.wins = [0,0]   #Example game attributes to maintain
        self.ties = 0   #Example game attributes to maintain
        self.moves = 0

    def get_player_move(self, p):
        return self.moves

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def winner(self):
        #determine who is the winner
        winner = True
        return winner

    def resetTurn(self):
        self.p1Went = False
        self.p2Went = False