#------------------------------------------------------------------------------
# main.py - main controller for playing game
#------------------------------------------------------------------------------

import view
import client
import sys
import utils

class Controller(object):
    """
    Main controller object to communicate between client module and user
    """
    def newGameWindow(self):
        """
        Create a new game Tk UI
        :return: GameWindow object, Tk root window
        """
        return view.GameWindow(newPlayerCallback=self.newPlayerCtrl,
                               requestCallback=self.submitPlayerMove)

    def newPlayerCtrl(self, playerColor):
        """
        Creates a player client to start communication with server
        :param playerColor: Player chosen color
        """
        self.newPlayer = client.Player(playerColor)
        self.newPlayer.newGame()

    def submitPlayerMove(self, move):
        """
        Make a request through the player client to server
        :param move: Players chosen Move
        :return: server's response to players move
        """
        try:
            return self.newPlayer.request(move.lower())
        except utils.ServerException, e:
            print e.message
            raise e

    def newRawGame(self):
        """
        Start a new game in terminal/commandline mode
        """
        print "\nChoose a Player Color."
        playerColor = raw_input("Red or Blue? ").lower()
        try:
            self.newPlayerCtrl(playerColor)
        except utils.ServerException, e:
            print e
            self.newRawGame()
        turnNum = 4
        while turnNum != 0:
            nextMoveMsg= "\nPlayer %s you have %d moves left.\n" \
                  "Pick your next move."
            print nextMoveMsg%(playerColor.title(), turnNum)
            playerOptions = utils.redOptions() if playerColor == 'red' else utils.blueOptions()
            playerOptions = [x.title() for x in playerOptions]
            playerMove = raw_input("%s "%playerOptions)
            try:
                responce = self.submitPlayerMove(playerMove)
            except utils.ServerException, e:
                continue
            print "%s Player picked %s"%(responce.get('computerColor').title(), responce.get('computerChoice').title())
            print "Red: %s\nBlue: %s"%(responce['score'].get('red'), responce['score'].get('blue'))
            turnNum += -1



if __name__ == "__main__":
    ctrl = Controller()

    if len(sys.argv) > 1:
        # Check if any sys arguments were passed in while starting the game.
        if sys.argv[1] == '--commandLine':
            # Check if the command line flag was used
            print utils.gameInstructions()
            print "Point System:"
            print utils.getPointSystem()
            print "Welcome!"
            ctrl.newRawGame()
        else:
            # if an unrecognized flag is used display the help instructions
            print utils.getHelp()
    else:
        # if no sys arguments are passed then run the UI mode of game using Tk
        ctrl.newGameWindow()