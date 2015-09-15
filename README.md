# Lodestar_Test

Simple turn-based, zero-sum game.
- You must first start server.py against python, which starts the game server with an AI player waiting to start a game. Make sure you don't exit this thread.
- Once the server is running then you can run main.py against python, which will start a Tk window, that'll allow you to start a new  game.
- Choose your player, and start the game. (hint: you'll never win, I made the AI too smart)
- The Tk window starts a client that can then communicate to the server.
- You can start as many Tk windows as you want, as there is no limit to how many clients can be running at the same time, communicating to the server.

TODO:  Commandline version of the game.


Game Play
- Pick a player color to start
- If you pick Red, you have the option of choosing 1 or 2 as your move.
- Since the computer in this case would be Blue, after your move it would pick between A, B, or C.
- Based on the selections you gain or lose points. ie. if Red chooses 1 and computer picks C, Red player would gain 20 point and Blue player would loose 20 points. The minimum score is 0.
- You have 4 moves to beat the computer. Good Luck! “ψ(｀∇´)ψ	
