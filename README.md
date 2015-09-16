# Lodestar_Test

Simple turn-based, zero-sum game.
- You must first start server.py against python, which starts the game server with an AI player waiting to start a game. Make sure you don't exit this thread.
- Once the server is running then you can run main.py against python, which will start a Tk window, that'll allow you to start a new  game.
- Choose your player, and start the game. (hint: you'll never win, I made the AI too smart)
- The Tk window starts a client that can then communicate to the server.
- You can start as many Tk windows as you want, as there is no limit to how many clients can be running at the same time, communicating to the server.

TODO:  Commandline version of the game.


Game Play
- Choose a red player or blue player to start.
- If you pick Red, you have the option of choosing 1 or 2 as your move.
- If you pick Blue, you have the option of choosing A, B, or C as your move.
- The Ai will always be your opponent, as the other color.
- In the window, the player's options are listed in the drop down menu.
- Based on the selection, you gain or lose points. e.g. if the Red player chooses 1 and Ai picks C, Red player would gain 20 point and Blue player would loose 20 points.
- For visual display, refer to the Point System Graph.
- You have 4 moves to beat the Ai. Winner takes all! Good Luck! “ψ(｀∇´)ψ	
