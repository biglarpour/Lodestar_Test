#------------------------------------------------------------------------------
# client.py - client for simple zero-sum game
#------------------------------------------------------------------------------

import zmq
import sys
import json
import time
import utils

PORT = utils.defaultServerPort()
HOST = utils.defaultHost()

class Player(object):
    def __init__(self, playerColor):
        self.playerColor = playerColor
        self.context = None
        self.redScore = 0
        self.blueScore = 0

    def newGame(self):
        if self.context is not None:
            self.context.term()
            self.redScore = 0
            self.blueScore = 0
        self.context = zmq.Context()
        print "Connecting to server..."
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://%s:%s" % (HOST, PORT))

    def request(self, playerChoice):
        #  Do a requests, waiting each time for a response
        playerData = {'playerColor':self.playerColor,
                      'playerChoice':playerChoice,
                      'score':{'red':self.redScore,
                               'blue':self.blueScore}}
        print "Sending request ", playerData,"..."
        self.socket.send (json.dumps(playerData))
        #  Get the reply.
        computerData = json.loads(self.socket.recv())
        time.sleep(1)
        newScore = computerData.get('score')
        self.redScore = int(newScore.get('red'))
        self.blueScore = int(newScore.get('blue'))
        return computerData