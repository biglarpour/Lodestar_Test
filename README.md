# Lodestar_Test

Simple turn-based, zero-sum game.
- You must first start server.py against python, which starts the game server with an AI player waiting to start a game. Make sure you don't exit this thread.
- Once the server is running then you can run main.py against python, which will start a Tk window, that'll allow you to start a new  game.
- Choose your player, and start the game. (hint: you'll never win, I made the AI too smart)
- The Tk window starts a client that can then communicate to the server.
- You can start as many Tk windows as you want, as there is no limit to how many clients can be running at the same time, communicating to the server.

TODO:  Commandline version of the game.
