import client_config
import socket
import threading
from game import Command
import time
import pickle
import queue

def ack(cmd):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    #Steps to handle this command

def join(cmd, _game):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    #Steps to handle this command

def whoami(cmd):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    client_config.user = cmd.cmd_data  
    client_config.user.connected = True
    # ISSUE:  May not be saving this User object globally on client??

def world(cmd, _game):
    print(f"     Processing {cmd.command} with {str(cmd.cmd_data)} world data")
    # NEED OBJECT FOR THE WORLD (Collection of Territories and Cards??)

def gm(cmd, _game):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    # NEED OBJECTS FOR THE GAME

def turn(cmd):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    # NEED TURN OBJECT

def territory(cmd):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    # NEED OBJECT FOR A TERRITORY (Collection of Territories and Cards??)

def take(cmd):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    # NEED OBJECT FOR A TERRITORY (Collection of Territories and Cards??)

def territories(cmd, mygame):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    # for t in cmd.cmd_data:
    #     print(t)

def adjacent(cmd, mygame):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    # NEED OBJECT FOR A TERRITORY (Collection of Territories and Cards??)

def players(cmd):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    client_config.players = cmd.cmd_data  

def armies(cmd):
    print(f"     Processing {cmd.command} with {cmd.cmd_data}")
    # WHAT OBJECT STORES ARMIES TO BE PLACED?

 