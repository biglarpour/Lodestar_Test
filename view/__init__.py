#------------------------------------------------------------------------------
# __init__.py - windows used to visualize game
#------------------------------------------------------------------------------

import functools
import utils
import Tkinter
import ttk

GAME_CONTENT = utils.getGameContent()

class GameWindow(Tkinter.Tk):
    def __init__(self, newPlayerCallback, requestCallback, *args, **kwargs):
        """
        Simple Tk UI to give visualization to game
        :param newPlayerCallback: Callback for when a new player is created
        :param requestCallback: Callback for when player makes a choice
        """
        Tkinter.Tk.__init__(self, *args, **kwargs)
        self.newPlayerCallback = newPlayerCallback
        self.requestCallback = requestCallback
        self.center(240, 80)
        self.title("You'll never win!")
        self.call('wm', 'attributes', '.', '-topmost', True)
        self.after_idle(self.call, 'wm', 'attributes', '.', '-topmost', False)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.initUi()
        self.lift()
        self.wait_window(self)

    def initUi(self):
        """
        Initialize the main UI and it's content based on player color
        :return:
        """
        self.frame = Tkinter.Frame(self)
        self.player = PlayerWindow(self, self.newPlayerCallback)
        self.playerColor = self.player.color
        self.center(700, 350)
        self.turnNumber = 4
        self.setScore()
        self.setComputerLabel()
        self.setPlayerLabel()
        Tkinter.Frame(self.frame,height=40,width=1,bg="lightgrey").grid(row=0, column=2, padx=15)
        self.setGameTable()
        self.setBtnBox()
        Tkinter.Label(self.frame, text=utils.gameInstructions(), anchor=Tkinter.W, justify=Tkinter.LEFT, wraplength=600).grid(row=8, columnspan=6)
        self.frame.pack()

    def setScore(self):
        """
        Setup for displaying score
        """
        self.scoreVar = Tkinter.StringVar()
        self.scoreVar.set("Red: 0\nBlue: 0")
        Tkinter.Label(self.frame, textvariable=self.scoreVar).grid(row=0)

    def setComputerLabel(self):
        """
        Setup label to represent responses from computer player
        """
        self.compLabelVar = Tkinter.StringVar()
        self.compLabelVar.set("You have first move.")
        Tkinter.Label(self.frame, textvariable=self.compLabelVar).grid(row=1)

    def setPlayerLabel(self):
        """
        Setup label to represent communicate info about and to active player
        """
        self.playerVar = Tkinter.StringVar()
        self.playerVar.set("Player %s has %d moves left"%(self.playerColor.title(), self.turnNumber))
        Tkinter.Label(self.frame, textvariable=self.playerVar).grid(row=2)
        self.playerOptions = utils.redOptions() if self.playerColor == 'red' else utils.blueOptions()
        self.playerOptions = [x.title() for x in self.playerOptions]
        self.playerOptions.insert(0, "Choose Move")
        self.var = Tkinter.StringVar()
        self.var.set(self.playerOptions[0])
        drop = Tkinter.OptionMenu(self.frame, self.var, *self.playerOptions, command=self.optionCallback)
        drop.grid(row=3)

    def setGameTable(self):
        """
        Setup for visually show case the point system that the game will use.
        """
        Tkinter.Label(self.frame, text="Point System Graph").grid(row=0, column=3)
        allRows = [[" ", "A", "B", "C"],
                   ["1", "30,-30", "-10, 10", "20,-20"],
                   ["2", "-10,10", "20,-20", "-20,20"]]
        for index, row in enumerate(allRows):
            for i, item in enumerate(row):
                color = 'red'
                if index == 0:
                    color = 'blue'
                itemList = item.split(",")
                if len(itemList) == 1:
                    f = Tkinter.Frame(self.frame, borderwidth=1, relief=Tkinter.SOLID)
                    Tkinter.Label(f, text=itemList[0], fg=color, width=10).pack(side=Tkinter.LEFT)
                else:
                    f = Tkinter.Frame(self.frame, borderwidth=1)
                    for splitIndex, eachItem in enumerate(itemList):
                        if splitIndex == 0:
                            color = 'red'
                        else:
                            color = 'blue'
                        Tkinter.Label(f, text=eachItem, fg=color).pack(side=Tkinter.LEFT)
                f.grid(row=index+1, column=i+3)

    def setBtnBox(self):
        """
        Setup New Game and Quit buttons
        """
        box = Tkinter.Frame(self.frame)
        ttk.Separator(self.frame, orient=Tkinter.HORIZONTAL).grid(row=6, columnspan=1, sticky="ew")
        w = Tkinter.Button(box,  text="New", width=7, command=self.restartGame)
        w.pack(side=Tkinter.LEFT)
        w = Tkinter.Button(box, text="Quit", width=7, command=self.close)
        w.pack(side=Tkinter.LEFT)
        box.grid(row=7)

    def restartGame(self):
        """
        callback to restart a new game
        """
        self.frame.destroy()
        self.initUi()

    def center(self, width, height):
        """
        Center the game to the center of screen and set it's size
        """
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.geometry("%sx%s+%d+%d" % (width, height, x, y))

    def optionCallback(self, *args):
        """
        Callback for when player has chosen an option
        Waits for response for server and sets all labels based on response
        """
        if self.turnNumber == 0:
            return
        playerChoice = self.var.get()
        if playerChoice == "Choose Move":
            return
        try:
            computerMove = self.requestCallback(playerChoice)
        except utils.ServerException, e:
            self.playerVar.set(e.message)
            return
        self.turnNumber = computerMove.get('turn')
        playerMessage = "Player %s has %d moves left"%(self.playerColor.title(), self.turnNumber)
        if computerMove.get('winner'):
            playerMessage = computerMove.get('winner')
        self.playerVar.set(playerMessage)
        self.compLabelVar.set("%s Player picked %s"%(computerMove.get('computerColor').title(), computerMove.get('computerChoice').title()))
        self.updateScore(computerMove.get('score'))
        self.var.set(self.playerOptions[0])

    def updateScore(self, scoreData):
        """
        updates the score board based on server response
        :param scoreData: score data received from server
        """
        self.scoreVar.set("Red: %s\nBlue: %s"%(scoreData.get('red'), scoreData.get('blue')))

    def close(self):
        """
        Close and destroy root tk window
        :return:
        """
        self.destroy()
        Tkinter.sys.exit(0)


class PlayerWindow(GameWindow, Tkinter.Toplevel):
    def __init__(self, parent, callback):
        """
        Simple Player Option window with
        :param parent: parent object to current window
        """
        Tkinter.Toplevel.__init__(self, parent)
        self.callback = callback
        self.transient(parent)
        self.parent = parent
        self.color = None
        self.initUi('Choose Player Color!')


    def initUi(self, title):
        """
        initialize ui elemnts
        :param title: window title
        """
        self.title(title)
        self.bodyF = Tkinter.Frame(self)
        self.initial_focus = self.body(self.bodyF)
        self.bodyF.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.center(248, 80)
        self.initial_focus.focus_set()
        self.wait_window(self)

    def buttonbox(self):
        """
        add standard button box with Red Player, and Blue Player
        """
        box = Tkinter.Frame(self)

        w = Tkinter.Button(box,  text="Red Player", width=10, command=functools.partial(self.setPlayerColor, 'red'))
        w.pack(side=Tkinter.LEFT, padx=5, pady=5)
        w = Tkinter.Button(box, text="Blue Player", width=10, command=functools.partial(self.setPlayerColor, 'blue'))
        w.pack(side=Tkinter.LEFT, padx=5, pady=5)

        box.pack()

    def setPlayerColor(self, color, *args, **kwargs):
        """
        Callback when player has chosen their color
        :param color: color chosen by player
        """
        self.color = color
        self.callback(self.color)
        self.cancel()

    def body(self, *args):
        pass

    def cancel(self, event=None):
        """
        close window and put focus back to the parent window
        """
        self.destroy()