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
    """
    Start the game server and wait for other players to join game
    """
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s" % (HOST, PORT))
    print "server started.."

    while True:
        #  Wait for next request from client
        gameData = json.loads(socket.recv())
        print "data recieved %s"%gameData
        score = gameData.get('score')
        try:
            computerData = getComputerChoice(gameData)
        except utils.ServerException, e:
            errorData = {"Error":e.message}
            socket.send(json.dumps(errorData))
            continue
        score[computerData['computerColor']] += computerData['points']
        computerData['score'] = score
        socket.send(json.dumps(computerData))
        print "responding with %s"%computerData

def getComputerChoice(data):
    """
    Based on other players choice make your move
    :param data: Dictionary object of data passed in from client, other players choice
    :return: Dictionary object with the best possible choice to win the game.
    """
    playerColor = data.get('playerColor')
    playerChoice = data.get('playerChoice')
    playerOptions = getattr(utils, '%sOptions'%playerColor.lower())()
    if not playerChoice in playerOptions:
        raise utils.ServerException("%s player picked an invalid option."%playerColor.title())
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