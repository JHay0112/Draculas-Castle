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
from tkinter import scrolledtext # Scrolled text element
import random # Generate random values

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
    COLUMN = 100 # Column height
    ROW = 100 # Row height

    # - __init__()
    # Initialise the game object
    #
    # self
    # game_map (rooms.Map) - The map the game is played in
    # boss_room_key (items.Key) - The key object that will unlock the boss room
    # enemies (list) - List containing enemy objects to be placed through the map
    # castle_items (list) - List containing item objects to be placed through the map
    def __init__(self, game_map, boss_room_key, enemies = None, castle_items = None):

        # Set attributes
        self._map = game_map
        self._parent = None # Stores tkinter parent object
        self._gui = None # Stores GUI object
        self._player = characters.Player("Player", game_map) # Initialise the player

        # For every item
        for item in castle_items:
            # Randomly select a room and add the item
            row = random.choice(self._map.grid())
            room = random.choice(row)
            room.inventory().add_item(item)

        # For every enemy
        for enemy in enemies:
            # Randomly select a room and add the enemy
            row = random.choice(self._map.grid())
            room = random.choice(row)
            room.add_enemy(enemy)

    # - gui()
    # Initialises the GUI aspect of the game
    #
    # self
    # parent (tkinter) - The GUI parent that the game exists in
    def gui(self, parent, height, width):

        #  Hold parent object
        self._parent = parent
        # + height and width
        self._height = height
        self._width = width

        # Add keystroke listeners
        self._parent.bind("w", self.move)
        self._parent.bind("s", self.move)
        self._parent.bind("a", self.move)
        self._parent.bind("d", self.move)

        # Initialise a new frame in the parent
        self._gui = tk.Frame(self._parent)
        self._gui.pack(fill = tk.BOTH)

        # Setup the map frame to show map in
        self._map_frame = tk.Frame(self._gui)
        self._map_frame.grid(row = 0, column = 0, rowspan = 4, columnspan = 4)
        # Setup the stat frame for the player
        self._player_stat_frame = tk.Frame(self._gui, height = Game.COLUMN, width = 2 * Game.ROW)
        self._player_stat_frame.grid(row = 0, column = 4, rowspan = 1, columnspan = 2)
        # Setup the stat frame for the enemy
        self._enemy_stat_frame = tk.Frame(self._gui, height = Game.COLUMN, width = 2 * Game.ROW)
        self._enemy_stat_frame.grid(row = 2, column = 4, rowspan = 1, columnspan = 2)
        # Setup the log frame
        self._log_frame = tk.Frame(self._gui, height = 2 * Game.COLUMN, width = 2 * Game.ROW)
        self._log_frame.grid(row = 3, column = 4, rowspan = 4, columnspan = 1)
        # Setup player inventory frame
        self._player_invent_frame = tk.Frame(self._gui, height = Game.COLUMN, width = 2 * Game.ROW)
        self._player_invent_frame.grid(row = 4, column = 0, columnspan = 2)
        # Setup room inventory frame
        self._room_invent_frame = tk.Frame(self._gui, height = Game.COLUMN, width = 2 * Game.ROW)
        self._room_invent_frame.grid(row = 4, column = 2, columnspan = 2)

        # Store current room
        self._current_room = self._player.room()
        # Set room use function to add item to player invent
        self._current_room.inventory().set_use_command(self._player.inventory().add_item)

        # Draw map
        self._current_room.gui(self._map_frame)
        
        # Setup player inventory
        self._player.inventory().gui(self._player_invent_frame)
        # Setup room inventory
        self._current_room.inventory().gui(self._room_invent_frame)

        # Setup text log
        self._log = scrolledtext.ScrolledText(self._log_frame,
                                              state = tk.DISABLED,
                                              width = 21,
                                              height = 18,
                                              wrap = tk.WORD)
        self._log.pack(fill = tk.BOTH, pady = (0, 10))

        # Log game start
        self.log("Welcome to Dracula's Castle!")

        # Refresh the GUI
        self.gui_refresh()

    # - gui_refresh()
    # Refreshes the GUI
    #
    # self
    def gui_refresh(self):

        # Check if the GUI is initialised
        if(self._gui != None):

             # Check if the room has changed
            if(self._current_room != self._player.room()):

                # Frames that will need cleared
                frames = [
                    self._map_frame,
                    self._room_invent_frame
                ]

                # Clear all frames
                for frame in frames:
                    # For every frame clear every widget that is a child of the frame
                    for widget in frame.winfo_children():
                        widget.destroy() # Destroy the child widget

                # Update current room
                self._current_room = self._player.room()
                # Set room use function to add item to player invent
                self._current_room.inventory().set_use_command(self._player.inventory().add_item)

                # Draw new map
                self._current_room.gui(self._map_frame)
                # Draw new inventory
                self._current_room.inventory().gui(self._room_invent_frame)

            # Draw player on map GUI
            self._current_room.draw_player(self._player)

    # - move()
    # Move the player as specified by key
    #
    # self
    # event (tkinter key event)
    def move(self, event):

        # Get representation of the event
        event = event.char

        # Interpret input
        if(event == "w"):
            # Move up
            self._player.move(-1, 0)
        elif(event == "s"):
            # Move down
            self._player.move(1, 0)
        elif(event == "a"):
            # Move left
            self._player.move(0, 1)
        elif(event == "d"):
            # Move right
            self._player.move(0, -1)

        # Refresh the GUI
        self.gui_refresh()

    # - log()
    # Logs an event to the text log
    #
    # self
    # text (str) - The text to log to the log
    def log(self, text):

        # Unlock log
        self._log.configure(state = tk.NORMAL)
        # Write to log
        self._log.insert(tk.INSERT, f"{text}\n")
        # Scroll to bottom
        self._log.see(tk.END)
        # Lock log
        self._log.configure(state = tk.DISABLED)

    # - rule_explanation()
    # GUI to explain the rules to the player
    #
    # self
    def rule_explanation(self):

        pass

    # - play_game()
    # Presents the player with the GUI game
    # 
    # self    
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

# --- Keys

# Key to Dracula's crypt
draculas_key = items.Key("THE KEY TO THE CRYPT")

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

# --- Collection of all items

castle_items = weapons
castle_items.extend(armour)
castle_items.extend(potions)

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
crypt = rooms.Room("THE CRYPT", key = draculas_key)

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
        cellar
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
    root.geometry("600x500+100+100")
    root.title("Dracula's Castle")

    # Game setup
    game = Game(castle_map, draculas_key, castle_enemies, castle_items) # Create game object
    game.gui(root, 600, 600)

    # Tkinter mainloop
    root.mainloop()
