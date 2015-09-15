#------------------------------------------------------------------------------
# __init__.py - windows used to visualize game
#------------------------------------------------------------------------------

import functools
import utils
from Tkinter import *
import ttk

GAME_CONTENT = utils.getGameContent()

class GameWindow(Tk):
    def __init__(self, newPlayerCallback, requestCallback, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.newPlayerCallback = newPlayerCallback
        self.requestCallback = requestCallback
        self.center(240, 80)
        self.lift()
        self.title("You'll never win!")
        self.call('wm', 'attributes', '.', '-topmost', True)
        self.after_idle(self.call, 'wm', 'attributes', '.', '-topmost', False)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.initUi()
        self.wait_window(self)

    def initUi(self):
        self.player = PlayerWindow(self, self.newPlayerCallback)
        self.playerColor = self.player.color
        self.center(600, 200)
        self.turnNumber=4
        self.setScore()
        self.setComputerLabel()
        self.setPlayerLabel()
        Frame(self,height=40,width=1,bg="lightgrey").grid(row=0, column=2, padx=15)
        self.setGameTable()
        self.setBtnBox()

    def setScore(self):
        self.scoreVar = StringVar()
        self.scoreVar.set("Red: 0\nBlue: 0")
        Label(self, textvariable=self.scoreVar).grid(row=0)

    def setComputerLabel(self):
        self.compLabelVar = StringVar()
        self.compLabelVar.set("You have first move.")
        Label(self, textvariable=self.compLabelVar).grid(row=1)

    def setPlayerLabel(self):
        self.playerVar = StringVar()
        self.playerVar.set("Player %s %d moves left"%(self.playerColor.title(), self.turnNumber))
        Label(self, textvariable=self.playerVar).grid(row=2)
        self.playerOptions = [1,2] if self.playerColor == 'red' else ['A', 'B', 'C']
        self.playerOptions.insert(0, "Choose Move")
        self.var = StringVar()
        self.var.set(self.playerOptions[0])
        drop = OptionMenu(self, self.var, *self.playerOptions, command=self.optionCallback)
        drop.grid(row=3)

    def setGameTable(self):
        Label(self, text="Point System").grid(row=0, column=3)
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
                    f = Frame(self, borderwidth=1, relief=SOLID)
                    Label(f, text=itemList[0], fg=color, width=10).pack(side=LEFT)
                else:
                    f = Frame(self, borderwidth=1)
                    for splitIndex, eachItem in enumerate(itemList):
                        if splitIndex == 0:
                            color = 'red'
                        else:
                            color = 'blue'
                        Label(f, text=eachItem, fg=color).pack(side=LEFT)
                f.grid(row=index+1, column=i+3)

    def setBtnBox(self):
        box = Frame(self)
        ttk.Separator(self, orient=HORIZONTAL).grid(row=6, columnspan=1, sticky="ew")
        w = Button(box,  text="New", width=7, command=self.restartGame)
        w.pack(side=LEFT)
        w = Button(box, text="Quit", width=7, command=self.close)
        w.pack(side=LEFT)
        box.grid(row=7)

    def restartGame(self):
        self.initUi()

    def center(self, width, height):
        """
        Center the home page to the center of screen
        """
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.geometry("%sx%s+%d+%d" % (width, height, x, y))

    def optionCallback(self, event=None):
        computerMove = self.requestCallback(self.var.get())
        self.turnNumber += -1
        self.playerVar.set("Player %s %d moves left"%(self.playerColor.title(), self.turnNumber))
        self.compLabelVar.set("%s Player picked %s"%(computerMove.get('computerColor'), computerMove.get('computerChoice').title()))
        self.updateScore(computerMove.get('score'))
        self.var.set(self.playerOptions[0])

    def updateScore(self, scoreData):
        self.scoreVar.set("Red: %s\nBlue: %s"%(scoreData.get('red'), scoreData.get('blue')))

    def close(self):
        self.destroy()
        sys.exit(0)


class PlayerWindow(GameWindow, Toplevel):
    def __init__(self, parent, callback):
        """
        Simple Player window with
        :param parent: parent object to current window
        """
        Toplevel.__init__(self, parent)
        self.callback = callback
        self.transient(parent)
        self.parent = parent
        self.color = None
        self.initUi('Chose Player Color!')


    def initUi(self, title):
        """
        initialize ui elemnts
        :param title: window title
        """
        self.title(title)
        self.bodyF = Frame(self)
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

    def body(self, master):
        """
        Need to implement main body
        """
        pass

    def buttonbox(self):
        """
        add standard button box with ok, and cancel
        """
        box = Frame(self)

        w = Button(box,  text="Red", width=10, command=functools.partial(self.setColor, 'red'))
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Blue", width=10, command=functools.partial(self.setColor, 'blue'))
        w.pack(side=LEFT, padx=5, pady=5)

        box.pack()

    def setColor(self, color, *args, **kwargs):
        """
        ok button event catcher
        """
        self.color = color
        self.callback(self.color)
        self.cancel()

    def cancel(self, event=None):
        """
        close window and put focus back to the parent window
        """
        self.destroy()