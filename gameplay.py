import pygame as pg
from geo import Country  #Will use World eventually
from player import Player
from dataclasses import dataclass

''' Gameplay operations:
    1 The Server receives client communications via multiple client specific socket threads
    2 Any one thread may not see this Game object and its functions
    3 Might need to pass each socket thread a pointer to a cmd queue []
    4 Messages received by a socket are simply appended to the end of the queue
    5 Server then pops and processes the front of the queue and so on...
'''

# Define a universal gameplay command, as a single object of class Command
class Command:
    def __init__(self, _id, _command, _cmd_data):
        self.id = _id  #player = originator of cmd
        self.command = _command  #command = an item from a command dictionary
        self.cmd_data = _cmd_data  #cmd_data = [] a list of key:values required for the command to execute

class Gameplay:
    def __init__(self):
        self.cmd_queue = []  # queue Client commands as received to sequence execution
        # Ideally client Sockets receiving a command msg, invokes a METHOD on the Gameplay Object
        # This queue may need to be passed to Socket Threads to store RECV'd Commands

    def append_cmd_queue(self, cmd):
        self.cmd_queue.append(cmd)  #add inbound Command to end of queue (really a list)
        print("Command added to queue:")
        print(cmd)
        self.validate_cmd(cmd)  #Take some steps to validate the Command
        self.process_cmd(cmd)  #Take steps to process the Command
        #Else this method would be bassed receive events from Socket Threads!  
        #Otherwise Gameplay will need a thread which loops to pick up cmds as they are queued

    def validate_cmd(cmd):
        #Need checks to assure this is a well formed Client Command
            # Does Player exist in Players[]?
            # Is it currently Player's turn?
            # Is this the right Turn.Step for this Client Command?
            # Are all the right data fields within the Command?
            # Does each data field check out?
        pass

    # Process gameplay commands
    def process_cmd(self, cmd):   #Send the cmd here **after** received on socket
        
        # **** MOVE ALL OF THIS TO THE SOCKET THREAD ****
        #raw_request = cmd.player.conn.recv(1024)   #Separate cmd 'receipt' code from 'process' code
        #if not raw_request:
        #    print("Empty msg received")
        #    break  # Empty message / What action to take?
        #cmd = raw_request.decode('utf-8')  # NO NOT REALLY THIS ********
        #print(f'Rquest from client: {request}')

        # Given a message from a client, figure out what to do with it...
        #Is is a Gameplay command vs an Administrative command??

        #Gameplay command processing:
        match(cmd.command):  #Switch on a flag within the Command object
            case 'name':
                print("'name' command received")
                response = self.name(cmd)
                #conn.send(bytearray(response, 'utf-8'))  #Rather, Send from Socket thread??
                #Add a broadcast command to share status

            case 'place':
                print("'place' command received")
                response = self.place(cmd)
                #client.send(bytearray(response, 'utf-8'))
                #Add a broadcast command to share status

            case 'fortify':
                print("'fortify' command received")
                response = self.fortify(cmd)
                #client.send(bytearray(response, 'utf-8'))
                #Add a broadcast command to share status

            case 'attack':
                print("'attack' command received")
                response = self.attack(cmd)
                #client.send(bytearray(response, 'utf-8'))
                #Add a broadcast command to share status
                
            case 'tmove':
                print("'tmove' command received")
                response = self.tmove(cmd)
                #client.send(bytearray(response, 'utf-8'))
                #Add a broadcast command to advance the turn
                
            case 'chat':
                print("'chat' command received")
                response = self.chat(cmd)
                #client.send(bytearray(response, 'utf-8'))
                #Add a broadcast command to advance the turn
                
            case _: 
                print("'unknown' command received")
                #response = self.unknown(cmd)
                #client.send(bytearray(response, 'utf-8'))

        #Supported for socket recv within process_cmd() - ** Moving this to Socket thread!!
        #except Exception as e:
        #    print(f'Problem processing client request: {e}')

    def name(self, cmd):
        cmd.player.name = "New name"  #Update SOR with new name
        #Send the updated Player object out to everyone

    def place(self, cmd):
        cmd.player.name = "New name"  #Update SOR with new name
        #Send the updated Player object out to everyone

    def fortify(self, cmd):
        cmd.player.name = "New name"  #Update SOR with new name
        #Send the updated Player object out to everyone

    def attack(self, cmd):
        cmd.player.name = "New name"  #Update SOR with new name
        #Send the updated Player object out to everyone

    def tmove(self, cmd):
        cmd.player.name = "New name"  #Update SOR with new name
        #Send the updated Player object out to everyone

    def chat(self, cmd):
        cmd.player.name = "New name"  #Update SOR with new name
        #Send the updated Player object out to everyone

    