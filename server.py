#------------------------------------------------------------------------------
# server.py - server for simple zero-sum game
#------------------------------------------------------------------------------

import zmq
import json
import utils

GAME_CONTENT = utils.getGameContent()
PORT = utils.defaultServerPort()
HOST = utils.defaultHost()

def start():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s" % (HOST, PORT))

    while True:
        #  Wait for next request from client
        gameData = json.loads(socket.recv())
        score = gameData.get('score')
        computerData = getComputerChoice(gameData)
        score[computerData['computerColor']] += computerData['points']
        computerData['score'] = score
        socket.send(json.dumps(computerData))

def getComputerChoice(data):
    playerColor = data.get('playerColor')
    playerChoice = data.get('playerChoice')
    if playerColor == 'blue':
        computerColor = 'red'
        computerChoices = GAME_CONTENT[computerColor].get(playerChoice)
        compPicked = max(computerChoices, key=lambda k: computerChoices[k])
        points = computerChoices[compPicked]
    else:
        computerColor = 'blue'
        computerChoices = GAME_CONTENT[computerColor]
        compPicked = max(computerChoices, key=lambda k: computerChoices[k].get(str(playerChoice)))
        points = computerChoices[compPicked].get(str(playerChoice))
    return {'computerChoice': compPicked,
            'computerColor': computerColor,
            'points': points}

if __name__ == "__main__":
    start()