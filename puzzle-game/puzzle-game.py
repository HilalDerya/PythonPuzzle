import tkinter as tk
from tkinter import simpledialog,messagebox
from PIL import ImageTk, Image
from random import shuffle, randrange

# Create linked list class
class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0
        self.tail = None
        
    # This function give us the size of the linked list
    def size(self):
        return self.length

    # This function prints the linked list objects
    def print(self): 
        current = self.head
        while current is not None:
            print(current.id, end=' -> ')
            current = current.next
        print('None')

    # Function to append new pieces in the list
    def append(self, piece):
        new_node = piece
        new_node.id = self.length
        self.length += 1
        if self.head == None:
            self.head = new_node
            return
        current_node = self.head
        while current_node.next is not None:
            current_node = current_node.next
        current_node.next = new_node

    # Function to insert piece in the list
    # without changing its id nor changing list size
    def _insert(self, position, piece):
        if position >= self.size():
            self.append(piece)
        current_node = self.head
        for i in range(position-1):
            current_node = current_node.next
        if position == 0:
            piece.next = self.head
            self.head = piece
        else:
            piece.next = current_node.next
            current_node.next = piece

    # Same as above but removing
    def _remove(self, id):
        current_node = self.head
        if current_node.id == id:
            self.head = self.head.next
            return
        while current_node.next is not None:
            if current_node.next.id == id:
                current_node.next = current_node.next.next
                return
            current_node = current_node.next

    # Function to get a piece's position in the list
    def get_position(self, id):
        current_node = self.head
        position = 0
        while current_node is not None:
            if current_node.id == id:
                return position
            current_node = current_node.next
            position += 1
        return -1

    # Function to get piece object at specified position
    def piece_at(self, pos):
        current_node = self.head
        i = 0
        while i < pos:
            current_node = current_node.next
            i += 1
        if current_node is None:
            print(f'Piece at {i} was None')
        return current_node

    # Function to get piece object with specified id
    def get_piece(self, id):
        current_node = self.head
        while current_node is not None:
            if current_node.id == id:
                return current_node
            current_node = current_node.next
        return None

    # Function to swap positions of two pieces in the list
    def swap(self, id1, id2):
        first = self.get_piece(id1)
        second = self.get_piece(id2)
        pos1 = self.get_position(id1)
        pos2 = self.get_position(id2)
        if first is None or second is None or first == second:
            return
        if pos1 > pos2:
            tmp = second
            second = first
            first = tmp
            tmp = pos2
            pos2 = pos1
            pos1 = tmp
        self._remove(id1)
        self._remove(id2)
        self._insert(pos1,second)
        self._insert(pos2,first)

    def shuffle(self):
        for i in range(self.size()):
            r = randrange(self.size())
            self.swap(i,r)

# Load the image
image = Image.open("image.jpg")

# Load scoreboard
scoreboard = []
try:
    score_file = open("enyuksekskor.txt", "r")
    for line in score_file:
        line = line.replace('\n',"") # removes possible newline characters
        scoreboard.append(line)
    score_file.close()
    print(len(scoreboard))
except FileNotFoundError as e:
    print("scoreboard file doesn't exist")

# [NOTE]
# classes have one purpose, to be able to hold variables/objects.
# it was pointless having both arrays, and references inside the class.
# so i removed them. use class only

class Piece:
    def __init__(self, image, row, col, locked=True): #CHANGED: locked=False
        self.image = image
        self.id = -1 #CHANGED: pieces have an id
        self.row = row
        self.col = col
        self.locked = locked
        self.next = None
        self.button = None  # Add the button attribute      

# Resize the image to fit the window
window_width = 1600
window_height = 900
aspect_ratio = image.width / image.height
if window_width / window_height < aspect_ratio:
    height = window_height
    width = int(height * aspect_ratio)
else:
    width = window_width
    height = int(width / aspect_ratio)
image = image.resize((width, height))

# Calculate the size of each piece
piece_width = image.width // 4
piece_height = image.height // 4

# Create a window
window = tk.Tk()
window.title("Puzzle Game")

# Split the image into 16 pieces
pieces = LinkedList()
for row in range(4):
    for col in range(4):
        x = col * piece_width
        y = row * piece_height
        box = (x, y, x + piece_width, y + piece_height)
        piece = image.crop(box)
        new_piece = Piece(ImageTk.PhotoImage(piece), row, col) #CHANGED: passing the PhotoImage object directly in the class
        # also, window must be created before this or it gives error.
        pieces.append(new_piece)

pieces.print()

# Create a grid of buttons to display the puzzle pieces
for i in range(pieces.size()):
    row = i // 4
    col = i % 4
    button = tk.Button(window, image=pieces.get_piece(i).image)
    button.grid(row=row, column=col)
    # Set the button attribute of the Piece object
    pieces.get_piece(i).button = button

# Define stats variables and their labels
username = None
score = 0
moves = 0
user_label = tk.Label(window)
user_label.grid(row=4, column=0)
score_label = tk.Label(window, text=f"Score: {score}")
score_label.grid(row=4, column=1)
moves_label = tk.Label(window, text=f'Moves: {moves}')
moves_label.grid(row=4, column=2)
first_click = None

# Define a function to handle button clicks
def button_click(row, col):
    print(f"Clicked: {row} {col}")
    global score, moves, first_click
    clicked_piece = pieces.piece_at((row * 4) + col)
    if clicked_piece.locked:
        return
    if first_click is None:
        first_click = clicked_piece
        first_click.button.config(relief="sunken")
        return
    else:
        second_click = clicked_piece
        first_click.button.config(relief="raised")
        if first_click == second_click:
            first_click = None
            return
            
        pieces.swap(first_click.id, second_click.id) # Swap pieces
        moves += 1
        
        # Changing button positions and callback functions
        for i in range(pieces.size()):
            piece = pieces.piece_at(i)
            row = i//4
            col = i%4
            piece.button.grid(row=row,column=col)
            piece.button.config(command=lambda r=row,c=col:button_click(r, c))
        
        # Check if the puzzle is solved
        solved = 0
        if first_click.id == pieces.piece_at(first_click.id).id:
            score += 5
        else:
            score -= 10
        for i in range(pieces.size()):
            piece = pieces.piece_at(i)
            if piece.id == i:
                solved += 1
                if piece.locked == False:
                    piece.locked = True
                    piece.button.config(relief='sunken')
                    # first_click was already handled
                    # so we skip it in the loop
                    if piece.id == first_click.id: 
                        continue
                    score += 5
        score_label.config(text=f"Score: {score}")
        moves_label.config(text=f"Moves: {moves}")
        first_click = None
        if solved == pieces.size():
            winner()

# Victory function. Shows top 5 players in the scoreboard to the user
def winner():
    global username,score,moves
    win = -1
    msg = 'Congratulations, you finished the game!\n\n'
    # Check if player's score is higher than players in the scoreboard
    for i,usr in enumerate(scoreboard):
        data = usr.split()
        if score >= int(data[1]):
            win = i
            break
    stri = f"{username} {score} {moves}"
    # Insert player in the scoreboard
    if win != -1:
        scoreboard.insert(win, stri)
    else:
        scoreboard.append(stri)
    
    # Setting messagebox string to list top 5 players
    for i,usr in enumerate(scoreboard):
        if i > 4:
            break
        data = usr.split()
        msg += f'{i+1}. {data[0]} = {data[1]} ({data[2]} moves)\n'
    # Update scoreboard file
    try:
        score_file = open("enyuksekskor.txt", "w")
        for i,line in enumerate(scoreboard):
            score_file.write(line+"\n") #adding newline
        score_file.close()
    except Exception as e:
        print(e)
    # Show messagebox
    tk.messagebox.showinfo('', msg)
    
# Create a "Shuffle" button
shuffle_button = tk.Button(window, text="Shuffle", bg='lightskyblue')
shuffle_button.grid(row=4, column=3)

# Define a function to shuffle the puzzle pieces
def shuffle_pieces():
    global score,username
    pieces.shuffle()
    for i in range(pieces.size()):
        piece = pieces.piece_at(i)
        piece.locked = False # CHANGED: unlocks pieces after shuffling
        piece.row = i // 4
        piece.col = i % 4
        # Update the positions of the pieces on the GUI
        row = i // 4
        col = i % 4
        piece.button.config(image=piece.image,command=lambda r=row,c=col: button_click(r,c))
        piece.button.grid(row=row, column=col)
    # Reset the score
    score = 0
    moves = 0
    score_label.config(text=f"Score: {score}")
    moves_label.config(text=f"Moves: {moves}")

    pieces.print()

# Function to get username
def get_username(self):
    global username, window
    # Unbind the event so the function runs only once
    window.unbind("<Visibility>")
    # Keep asking until the user gives an input
    while username is None or username == '':
        username = tk.simpledialog.askstring('Hello','Insert your name',parent=window)
    user_label.config(text=f"Username: {username}")
    

# Bind the "Shuffle" button to the shuffle_pieces function
shuffle_button.config(command=shuffle_pieces)

# Run get_username function when window becomes visible
# (so dialog appears on top)
window.bind("<Visibility>", get_username)

# Run the event loop
window.mainloop()