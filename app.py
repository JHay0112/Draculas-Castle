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
    # game_map (rooms.Map) - The map the game is played in
    def __init__(self, game_map):

        # Set attributes
        self._map = game_map
        self._parent = None # Stores tkinter parent object
        self._gui = None # Stores GUI object

    # - gui()
    # Initialises the GUI aspect of the game
    #
    # self
    # parent (tkinter) - The GUI parent that the game exists in
    def gui(self, parent):

        pass

    def rule_explanation(self):

        pass

    def player_customisation(self):

        pass

    def play_game(self):

        pass

    # - battle()
    # Battle the player and an enemy
    #
    # self
    # enemy (characters.Enemy) - The enemy the player will do battle with
    def battle(self, enemy):

        pass

# - Main

root = tk.Tk() # Tkinter root object

# -- Items

# --- Weapons

weapons = [
        items.Weapon("Pointy Stick", 2, 5),
        items.Weapon("Crowbar", 3, 8),
        items.Weapon("Steaming Vat of Molten Cheese", 5, 9),
        items.Weapon("Nokia 3310 Boomerang", 10, 15),
        items.Weapon("Laser Jet Printer", 12, 18)
    ]

# --- Armour

armour = [
        items.Armour("MDF Shield", 5),
        items.Armour("Sheet Metal Shield", 6),
        items.Armour("Wooden Breastplate", 7),
        items.Armour("Sheet Metal Breastplate", 10),
        items.Armour("Nokia 3310 Shin Pads", 15)
    ]

# --- Potions

potions = [
        items.Potion("Water", 5),
        items.Potion("Bathwater?", -5),
        items.Potion("Fresh Mountain Water", 20),
        items.Potion("Hot Chocolate", 10)
    ]

# -- Enemies

# Dracula
dracula = characters.Enemy("COUNT DRACULA",
                           1000,
                           items.Weapon("DRACULA'S STAFF", 50, 100),
                           items.Armour("DRACULA'S SHIELD", 100))

# Other enemies that can be found in the castle
castle_enemies = [
        characters.Enemy("The Goose",
                         50,
                         items.Weapon("HONK", 15, 20),
                         items.Armour("Goose Feathers", 10)),
        characters.Enemy("Thousands of Bees",
                         100,
                         items.Weapon("Sting", 1, 3),
                         items.Armour("Exoskeleton", 1),
                         [items.Weapon("Bee Sting Sword", 10, 25),
                          items.Potion("Honey", 20)]),
        characters.Enemy("John",
                         20,
                         items.Weapon("Steak Knife", 5, 10),
                         items.Armour("Torn Jeans", 3),
                         [items.Potion("Homebrew", 10)]),
        characters.Enemy("SyntaxError",
                         5,
                         items.Weapon("Inconvenience", 1, 10))
    ]

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
    game = Game(castle_map) # Create game object

    # Tkinter mainloop
    root.mainloop()
