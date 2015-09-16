# Lodestar_Test

Simple turn-based, zero-sum game.
- You must first start server.py against python, which starts the game server with an AI player waiting to start a game. Make sure you don't exit this thread. e.g. python server.py
- Once the server is running then you can run main.py against python.
- To start the game in UI mode, which will start a Tk window, execute with no flags. e.g. python main.py
- To start the game in command line mode, recommended to run in terminal, execute with --commandLine flag. e.g. python main.py --commandLine
- Choose your player, and start the game. (hint: you'll never win, I made the AI too smart)
- Once a player has been selected a player client is started and connects to the running server, which can then start to send messages back and forth.
- You can start as many games as you wish, as there is no limit to how many clients can be running at the same time, communicating to the server.

Written and tested in OSX 10.9.5 and Python2.7

Game Play
- Choose a red player or blue player to start.
- If you pick Red, you have the option of choosing 1 or 2 as your move.
- If you pick Blue, you have the option of choosing A, B, or C as your move.
- The Ai will always be your opponent, as the other color.
- In the window, the player's options are listed in the drop down menu.
- Based on the selection, you gain or lose points. e.g. if the Red player chooses 1 and Ai picks C, Red player would gain 20 point and Blue player would loose 20 points.
- For visual display, refer to the Point System Graph.
- You have 4 moves to beat the Ai. Winner takes all! Good Luck! “ψ(｀∇´)ψ	

