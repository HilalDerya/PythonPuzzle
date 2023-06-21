# Puzzle Game
This is a simple puzzle game created using Python and the Tkinter library. The game consists of 16 pieces that are shuffled and then the player must move them around to form the original image. Each move is scored, and the player with the highest score at the end wins.

# How To Play
To start the game, run the puzzle_game.py script using Python. The game window will open, and you will be prompted to enter your name. Once you enter your name, the game will start.
The puzzle pieces will be shuffled, and you can start moving them around by clicking on a piece and then clicking on an adjacent piece to swap them. You can only move unlocked pieces. If you manage to put all the pieces in their correct position, you win!
Your score is calculated based on the number of moves you make. Each correct move adds 5 points to your score, while each incorrect move deducts 10 points from your score.
You can shuffle the pieces at any time by clicking the "Shuffle" button. You can also view the top scores by clicking the "Scoreboard" button.

# Scoreboard
The game reads and writes the top scores to a file called "enyuksekskor.txt" The file should contain one score per line, in the format. The game will display the top scores in a message box when the "Scoreboard" button is clicked.
