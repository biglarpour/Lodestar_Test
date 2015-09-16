#------------------------------------------------------------------------------
# client.py - client for simple zero-sum game
#------------------------------------------------------------------------------

import zmq
import json
import utils

PORT = utils.defaultServerPort()
HOST = utils.defaultHost()

class Player(object):
    def __init__(self, playerColor):
        """
        Simple client object used to communicate to server
        :param playerColor: The active players color. options red, or blue
        """
        self.playerColor = playerColor
        if not self.playerColor.lower() in utils.getGameContent().keys():
            raise utils.ServerException("Invalid player color %s"%self.playerColor)
        self.context = None
        self.redScore = 0
        self.blueScore = 0
        self.turn = 4
        self.timeout = 10

    def newGame(self):
        """
        Start a new connection to the server to send messages back and forth
        """
        if self.context is not None:
            self.context.term()
            self.redScore = 0
            self.turn = 0
            self.blueScore = 0
        self.context = zmq.Context()
        print "Connecting to server..."
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.connect("tcp://%s:%s" % (HOST, PORT))

    def request(self, playerChoice):
        """
        Send the server the players choice and wait for a response.
        The request is sent to the server as a json dumped object.
        :param playerChoice: The input move chosen by active player
        :return: A dictionary object from the server side computer players
                 responding to the active players choice.
        """
        #  Do a requests, waiting each time for a response
        playerData = self.buildPlayerData(playerChoice)
        print "Sending request ", playerData,"..."
        self.socket.send(playerData)

        #  Get the reply.
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)
        if poller.poll(10*1000):
            computerData = json.loads(self.socket.recv())
        else:
            raise utils.ServerException("Timeout processing, is the server running?")
        if computerData.get("Error"):
            raise utils.ServerException(computerData.get("Error"))

        self.setNewScore(computerData)

        # adjust the turn counter and check if anyone has won.
        self.turn += -1
        additionalData = {'turn': self.turn}
        if self.turn == 0:
            winningMsg = "Game Over! %s Player Wins!!!"%("Red" if self.redScore > self.blueScore else "Blue")
            print winningMsg
            additionalData["winner"]= winningMsg

        computerData.update(additionalData)
        return computerData

    def buildPlayerData(self, playerChoice):
        """
        Build players choice data to be sent to server
        :param playerChoice: The input move chosen by active player
        :return: a json dump string of data to be sent to server
        """
        return json.dumps({'playerColor':self.playerColor,
                           'playerChoice':playerChoice,
                           'score':{'red':self.redScore,
                           'blue':self.blueScore}})

    def setNewScore(self, computerData):
        """
        Sets the new score based on points returned by server
        :param computerData: Dictionary data sent over from server
        """
        newScore = computerData.get('score')
        self.redScore = int(newScore.get('red'))
        self.blueScore = int(newScore.get('blue'))