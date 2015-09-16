#------------------------------------------------------------------------------
# utils.py -  utilities for simple zero-sum game
#------------------------------------------------------------------------------
import json
import sys
import os
ROOTFOLDER = os.path.dirname(sys.argv[0])

BCOLORS={'blue' : '\033[94m',
         'red' : '\033[91m',
         'end' : '\033[0m'}

class ServerException(Exception):
    """
    Generic exception for server side error handling to be caught by client
    """
    pass

def getGameContent():
    """
    Loads the game data as a json object
    :return: a dictionary object with all needed data to build game
    """
    with open("%s/gameData.json"%ROOTFOLDER, 'r') as _file:
        return json.load(_file)

def defaultServerPort():
    """
    :return: default server port to connect to. Used by zmq
    """
    return 5556

def defaultHost():
    """
    :return: default host to connect to. Used by zmq
    """
    return "127.0.0.1"

def redOptions():
    """
    :return: Possible options for red player to choose
    """
    return ['1','2']

def blueOptions():
    """
    :return: Possible options for blue player to choose
    """
    return ['a', 'b', 'c']

def gameInstructions():
    return """
Instructions

- Choose a red player or blue player to start.
- If you picked Red, you have the option of choosing 1 or 2 as your move.
- If you picked Blue, you have the option of choosing A, B, or C as your move.
- The Ai will always be your opponent, as the other color.
- In the window, the player's options are listed in the drop down menu.
- Based on the selection, you gain or lose points. e.g. if the Red player chooses 1 and Ai picks C, Red player would gain 20 point and Blue player would loose 20 points.
- For visual display, refer to the Point System Graph.
- You have 4 moves to beat the Ai. Winner takes all! Good Luck!
"""

def getHelp():
    return """
Options:

To run the Gui version of the game run with no flags.

Flags:

--commandLine: To run game in command line mode

%s
%s
"""%(gameInstructions(), getPointSystem())

def getPointSystem():
    return """
    |    %(blue)sA%(end)s    |    %(blue)sB%(end)s    |    %(blue)sC%(end)s    |
-----------------------------------
  %(red)s1%(end)s | %(red)s30%(end)s, %(blue)s-30%(end)s | %(red)s-10%(end)s, %(blue)s10%(end)s | %(red)s20%(end)s, %(blue)s-20%(end)s |
-----------------------------------
  %(red)s2%(end)s | %(red)s10%(end)s, %(blue)s-10%(end)s | %(red)s20%(end)s, %(blue)s-20%(end)s | %(red)s-20%(end)s, %(blue)s20%(end)s |
-----------------------------------
"""%BCOLORS
