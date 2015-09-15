#------------------------------------------------------------------------------
# main.py - main ui for playing game
#------------------------------------------------------------------------------

import view
import client

class Controller(object):
    def newGameWindow(self):
        return view.GameWindow(newPlayerCallback=self.newPlayerCtrl,
                               requestCallback=self.submitPlayerMove)

    def newPlayerCtrl(self, playerColor):
        self.newPlayer = client.Player(playerColor)
        self.newPlayer.newGame()

    def submitPlayerMove(self, move):
        return self.newPlayer.request(move.lower())

if __name__ == "__main__":
    ctrl = Controller()
    ctrl.newGameWindow()