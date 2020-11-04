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
from tkinter import messagebox # Message boxes for errors
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
        self._boss_room_key = boss_room_key # Store key of boss room
        self._parent = None # Stores tkinter parent object
        self._gui = None # Stores GUI object
        self._player_name = tk.StringVar()
        self._player_age = tk.IntVar()
        self._player = characters.Player("Player", game_map) # Initialise the player
        self._control_state = True # Stores the state of the controls

        # Set boss room key callback
        self._boss_room_key.set_callback(self.unlock_boss_room)

        # Default values for player name/age
        self._player_name.set("Player")
        self._player_age.set(18)

        # Add boss room key to items
        castle_items.append(self._boss_room_key)

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
        # Setup text log
        self._log = scrolledtext.ScrolledText(self._log_frame,
                                              state = tk.DISABLED,
                                              width = 21,
                                              height = 16,
                                              wrap = tk.WORD)
        self._log.pack(fill = tk.X)
        # Setup log control frame
        self._log_controls = tk.Frame(self._log_frame, height = 20)
        self._log_controls.pack(fill = tk.X, pady = (2, 5))
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

        # Setup player stat frame
        self._player.gui(self._player_stat_frame)

        # Setup control buttons
        self._attack = ttk.Button(self._log_controls, text = "ATTACK", state = tk.DISABLED)
        self._attack.pack(fill = tk.X, side = tk.LEFT, expand = True)
        self._retreat = ttk.Button(self._log_controls, text = "RETREAT", state = tk.DISABLED, command = self.retreat)
        self._retreat.pack(fill = tk.X, side = tk.LEFT, expand = True)

        # Log game start
        self.log("Welcome to Dracula's Castle!")

        # Print out a tutorial in log
        self.log("""Use WASD to move.""")

        # Withdraw parent window
        self._parent.withdraw()

        # Get player info
        # Setup window
        self._player_info_window = tk.Toplevel(self._parent, padx = 10, pady = 10)
        self._player_info_window.title("Character Creation")
        self._player_info_window.geometry("200x150+100+100")
        # Setup widgets
        # Set title
        tk.Label(self._player_info_window, text = "Character Creation", anchor = tk.W).pack(fill = tk.X)
        # Name label
        tk.Label(self._player_info_window, text = "Name:", anchor = tk.W).pack(fill = tk.X)
        # Name input
        tk.Entry(self._player_info_window, textvariable = self._player_name).pack(fill = tk.X)
        # Age label
        tk.Label(self._player_info_window, text = "Age:", anchor = tk.W).pack(fill = tk.X)
        # Age input
        tk.Entry(self._player_info_window, textvariable = self._player_age).pack(fill = tk.X)
        # Set button
        ttk.Button(self._player_info_window, text = "Create Character", command = self.update_player).pack(fill = tk.X, pady = (5, 0))
        # Focus
        self._player_info_window.focus_force()

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

                # Store previous room
                self._previous_room = self._current_room
                # Update current room
                self._current_room = self._player.room()
                # Set room use function to add item to player invent
                self._current_room.inventory().set_use_command(self.give_player_item)

                # Draw new map
                self._current_room.gui(self._map_frame)
                # Draw new inventory
                self._current_room.inventory().gui(self._room_invent_frame)

                # Room has changed so we should check if there are any enemies
                if(self._current_room.enemies() != []):
                    # BATTLE! (first enemy only):
                    self.battle(self._current_room.enemies()[0])

            # Draw player on map GUI
            self._current_room.draw_player(self._player)

    # - update_player()
    # Updates the player info from character selection
    #
    # self
    def update_player(self):
            
        # Flag for errors
        error = False

        # Get inputs
        name = self._player_name.get() # Get name, should always run without error
        # Try and get age, if non-int with throw exception
        try:
            age = int(self._player_age.get())
        except:
            # Age is not int, alert user!
            messagebox.showerror("ERROR", "Age must be an integer (whole number e.g. 3)!")
            error = True

        # Check that age is above zero
        if(age <= 0):
            # Age is invalid
            messagebox.showerror("ERROR", "Age must be above zero (e.g. 3)!")
            error = True

        # If age is greater than 10000
        if(age > 10000):
            # It's starting to get ridiculous, we'll limit this
            messagebox.showerror("ERROR", "Age must be 10000 or less (e.g. 3)!")
            error = True

        # If name length is greater than 15 characters
        if(len(name) > 15):
            # Name is unreasonably long
            messagebox.showerror("ERROR", f"Name must be no longer than 15 characters (It is currently {len(name)})!")
            error = True
            
        # Only run these if there are no errors
        if(not error):
            # Send values to player object
            self._player.set_name(name)
            self._player.set_age(age)

            # Close player creation dialogue
            self._player_info_window.destroy()
            # Open main window
            self._parent.deiconify()
            # Make sure parent is focused
            self._parent.focus_force()

    # - give_player_item()
    # Give the player an item
    #
    # self
    # item (items.Item) - The item to add
    def give_player_item(self, item):

        # Check if it's a key
        if(type(item) == items.Key):
            # Players cannot "use" keys
            # Disable useability
            item.set_useable(False)
            # Run key callback
            item.use()

        # Add to inventory
        self._player.inventory().add_item(item)

    # - move()
    # Move the player as specified by key
    #
    # self
    # event (tkinter key event)
    def move(self, event):

        # Check control state
        if(self._control_state == True):

            # Only runs if controls enabled

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

    # - set_control_state()
    # Sets the control state
    #
    # self
    # new_state (bool) - The state to set the controls to
    def set_control_state(self, new_state):

        self._control_state = new_state

    # - log()
    # Logs an event to the text log
    #
    # self
    # text (str) - The text to log to the log
    def log(self, text):

        # Unlock log
        self._log.configure(state = tk.NORMAL)
        # Write to log
        self._log.insert(tk.END, f"{text}\n\n")
        # Scroll to bottom
        self._log.see(tk.END)
        # Lock log
        self._log.configure(state = tk.DISABLED)

    # - attack()
    # Player attack enemy
    #
    # self
    # enemy (characters.Enemy) - The enemy to battle with
    def attack(self, enemy):

        # Attack the enemy
        attack_dam = self._player.attack(enemy)

        # Log the attack
        self.log(f"You did {attack_dam} damage to {enemy.name()}.")
        
        # Check if enemy is still alive
        if(enemy.is_alive() != True):
            # Enemy is dead and you have killed them
            self.log(f"{enemy.name()} is dead and you have killed them.")
            # Drop their inventory into the room
            self._current_room.inventory().add_items(enemy.drop_inventory())
            # Refresh the GUI
            self.gui_refresh()
            # Remove enemy from room
            self._current_room.enemies().remove(enemy)
            # Unlock controls
            self.set_control_state(True)
            # Lock log controls
            self._attack.configure(state = tk.DISABLED)
            self._retreat.configure(state = tk.DISABLED)
            # Remove enemy GUI
            for widget in self._enemy_stat_frame.winfo_children():
                widget.destroy()

            # Check if in the boss room
            if(self._current_room == self._map.boss_room()):
                # This means the boss is dead!
                messagebox.showinfo("CONGRATULATIONS!", f"You killed {enemy.name()}!")
                # Remove GUI
                self._parent.destroy()
        else:
            # Else the enemy attacks you
            attack_dam = enemy.attack(self._player)

            # Log the attack
            self.log(f"{enemy.name()} did {attack_dam} damage to you!")

            # Check if you're still alive
            if(self._player.is_alive() != True):
                
                # Check if fighting boss
                if(self._current_room == self._map.boss_room()):
                    # You are dead forever now
                    # Tell the user
                    messagebox.showinfo("DEFEAT!", f"{enemy.name()} killed you! This is the end.")
                    # Remove GUI
                    self._parent.destroy()
                else:
                    # Not fighting boss, revive
                    # YOU DIED!
                    self.log(f"You were incapacitated by {enemy.name()}!")
                    # Retreat
                    self.retreat()
                    # Give the player some health back
                    self._player.take_damage(-10)
                    # Unlock controls
                    self.set_control_state(True)
                    # Lock log controls
                    self._attack.configure(state = tk.DISABLED)
                    self._retreat.configure(state = tk.DISABLED)
                
    # - retreat()
    # Retreat from an enemy
    #
    # self
    def retreat(self):

        # Log the retreat
        self.log("You retreated!")
        # Move the player back one room
        self._player.change_room(self._previous_room, "m")
        # Turn on map controls
        self.set_control_state(True)
        # Disable log control buttons
        self._attack.configure(state = tk.DISABLED)
        self._retreat.configure(state = tk.DISABLED)
        # Refresh GUI
        self.gui_refresh()
        # Remove enemy GUI
        for widget in self._enemy_stat_frame.winfo_children():
            widget.destroy()

    # - battle()
    # Battle the player and an enemy
    #
    # self
    # enemy (characters.Enemy) - The enemy the player will do battle with
    def battle(self, enemy):

        # Turn off map controls
        self.set_control_state(False)
        # Turn on log control buttons
        self._attack.configure(state = tk.NORMAL, command = lambda e = enemy : self.attack(e))
        self._retreat.configure(state = tk.NORMAL)
        # Tell the user they have been attacked
        self.log(f"You are attacked by {enemy.name()}!")

        # Initiate enemy gui
        enemy.gui(self._enemy_stat_frame)

    # - unlock_boss_room()
    # Unlocks the boss room
    #
    # self
    def unlock_boss_room(self):

        # Flag for if an entrance has been added
        entrance_added = False

        self.log("THE CRYPT HAS BEEN UNLOCKED!")

        # Add entrance to the crypt to a random room
        while(entrance_added != True):

            # Pick a random room from the set of rooms
            row = random.choice(self._map.grid())
            room = random.choice(row)

            # Check if there are any free entrances
            for entrance_name, entrance_val in room.entrances().items():
                # Entrance value will be false if no entrance exists there
                if(entrance_val == False):
                    # Add the entrance
                    room.add_entrance(entrance_name, self._map.boss_room())
                    # Set flag true to exit loop
                    entrance_added = True
                    break # Break for loop

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
        items.Weapon("Molten Cheese", 5, 9),
        items.Weapon("Boomerang", 10, 15),
        items.Weapon("Laser Jet Printer", 12, 18),
        items.Weapon("Red Syringe", 10, 25)
    ]

# --- Armour

armour = [
        items.Armour("MDF Shield", 5),
        items.Armour("Sheet Metal Shield", 6),
        items.Armour("Wooden Breastplate", 7),
        items.Armour("Sheet Metal Breastplate", 10),
        items.Armour("Shin Pads", 15)
    ]

# --- Potions

potions = [
        items.Potion("Water", 5),
        items.Potion("Fresh Mountain Water", 20),
        items.Potion("Hot Chocolate", 10),
        items.Potion("Sustenance Bar", 30),
        items.Potion("Green Syringe", 50)
    ]

# --- Collection of all items

castle_items = weapons
castle_items.extend(armour)
castle_items.extend(potions)

# -- Enemies

# Dracula
dracula = characters.Enemy("COUNT DRACULA",
                           1000,
                           100,
                           items.Weapon("DRACULA'S STAFF", 30, 50),
                           items.Armour("DRACULA'S SHIELD", 20))

# Other enemies that can be found in the castle
castle_enemies = [
        characters.Enemy("The Goose",
                         2,
                         40,
                         items.Weapon("HONK", 10, 15),
                         items.Armour("Goose Feathers", 10)),
        characters.Enemy("Thousands of Bees",
                         1,
                         100,
                         items.Weapon("Sting", 1, 3),
                         items.Armour("Exoskeleton", 1),
                         [items.Weapon("Bee Sting Sword", 20, 30),
                          items.Potion("Honey", 20)]),
        characters.Enemy("John",
                         32,
                         20,
                         items.Weapon("Steak Knife", 5, 10),
                         items.Armour("Torn Jeans", 3),
                         [items.Potion("Homebrew", 10)]),
        characters.Enemy("SyntaxError",
                         1,
                         5,
                         items.Weapon("Inconvenience", 1, 10)),
        characters.Enemy("The Beekeeper",
                         48,
                         20,
                         items.Weapon("Smoker", 1, 15),
                         items.Armour("Beekeeping Suit", 3),
                         [items.Potion("Honeycomb", 30), items.Weapon("Pry Tool", 5, 20)]),
        characters.Enemy("Larry",
                         10,
                         15,
                         items.Weapon("Advice", -10, 10),
                         None),
        characters.Enemy("Imaginos",
                         100,
                         30,
                         items.Weapon("Staff of the Ether", 10, 20),
                         None,
                         [items.Potion("Ether", 50)])
    ]

# -- Map/Rooms

# Special rooms
toilet = rooms.Room("Toilet", s = True)
cellar = rooms.Room("Cellar", n = True, w = toilet)
entrance_hall = rooms.Room("Entrance Hall", n = True)
crypt = rooms.Room("THE CRYPT")
crypt.add_enemy(dracula) # Add dracula to the crypt

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
