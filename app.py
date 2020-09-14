'''

    app.py

    Author: Jordan Hay
    Date: 2020-09-06

    Dracula's Castle application/game

'''

# - Imports

# -- Libraries
# (Modules others have made)
import tkinter as tk # GUI
from tkinter import ttk # Refined GUI elements

# -- Components
# (Modules I have made)
import items # Items/Inventories
import rooms # Maps/Rooms
import characters # Player/Enemies

# - Classes

# - Game
# The game object, controls all aspects of a game
class Game:

    # Game Constants
    EASY = 0.5
    NORMAL = 1
    HARD = 1.5

    # - __init__()
    # Initialise the game object
    #
    # self
    # parent (tkinter) - Parent GUI Object
    # game_map (rooms.Map) - The map the game is played in
    def __init__(self, parent, game_map):

        pass

# - Main

root = tk.Tk() # Tkinter root object

# -- Map/Rooms

# Special rooms
toilet = rooms.Room("Toilet", s = True)
cellar = rooms.Room("Cellar", n = True, w = toilet)
entrance_hall = rooms.Room("Entrance Hall", n = True)
crypt = rooms.Room("THE CRYPT")

# Create Map of rooms
castle_map = rooms.Map([
    [
        rooms.Room("Dressing Room", e = True, s = True), 
        rooms.Room("Bathroom", w = True), 
        rooms.Room("Sun Room", s = True), 
        rooms.Room("Kitchen", s = True, e = True), 
        rooms.Room("Pantry", w = True)
    ],
    [
        rooms.Room("Bedroom", n = True, s = True), 
        toilet, 
        rooms.Room("Back Hall", n = True, s = True, e = True), 
        rooms.Room("Passage", n = True, w = True, e = True),
        rooms.Room("Scullery", s = True, w = True)
    ],
    [
        rooms.Room("West Tower", n = True, s = True, e = True),
        rooms.Room("West Hallway", n = True, e = True, w = True),
        rooms.Room("Main Hall", n = True, s = True, e = True, w = True),
        rooms.Room("Corridor", s = True, w = True),
        rooms.Room("Cellar", n = True)
    ],
    [
        rooms.Room("Drawing Room", n = True, e = True),
        rooms.Room("Library", w = True),
        entrance_hall,
        rooms.Room("Lounge", n = True, e = True),
        rooms.Room("East Tower", w = True)
    ]
], entrance_hall, crypt)

# Main check
if __name__ == "__main__":

    # Tkinter setup
    root.geometry("1000x700+100+100")
    root.title("Dracula's Castle")

    # Game setup
    game = Game(root, castle_map) # Create game object

    # Tkinter mainloop
    root.mainloop()
