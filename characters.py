'''

    characters.py

    Author: Jordan Hay
    Date: 2020-09-07

    Characters, e.g. the player, enemies, in Dracula's Castle

'''

# - Imports

import items # Create items
import rooms # Manage rooms
import tkinter as tk # GUI
from tkinter import ttk # Refined GUI elements

# - Classes

# - Character
# The base for both players and enemies
class Character:

    # - __init__()
    #
    # self
    # name (str) - The name of the character
    # health (int) - The health of the character
    # weapon (items.Weapon) - The weapon the character uses
    # armour (items.Armour) - The armour the character uses
    # items (list) - List of items to add to the character's inventory
    def __init__(self, name, health = 100, weapon = None, armour = None, invent_items = None):

        # Set attributes
        self._name = name
        self._inventory = items.Inventory() 
        self._weapon = weapon
        self._armour = armour
        self._health = health
        self._gui = None

        # Add items to inventory
        if(type(invent_items) == list):
            self._inventory.add_items(invent_items)

    # - name()
    # Returns the name of the character
    #
    # self
    def name(self):

        return(self._name)

    # - weapon()
    # Returns the weapon object the enemy uses
    #
    # self
    def weapon(self):

        return(self._weapon)

    # - armour()
    # Returns the armour object the character uses
    #
    # self
    def armour(self):

        return(self._armour)

    # - inventory()
    # Returns the inventory object of the character
    #
    # self
    def inventory(self):

        return(self._inventory)

    # - is_alive()
    # Returns whether the character is still alive
    #
    # self
    def is_alive(self):

        # Check if health is less than or equal to 0
        if(self._health <= 0):
            # If so return false
            return(False)
        else:
            # Else return true
            return(True)

    # - drop_inventory()
    # Returns all items in player, intended for on the character's death
    #
    # self
    def drop_inventory(self):

        # Get armour and weapon and put in inventory
        # Check that they're not none first
        if(self._weapon != None):
            self._inventory.add_item(self._weapon)
        if(self._armour != None):
            self._inventory.add_item(self._armour)

        # Get list of items in inventory
        invent_items = self._inventory.items()

        # Wipe inventory
        self._inventory.drop_all()

        return(invent_items)

    # - take_damage()
    # Applies an amount of damage to the character
    #
    # self
    # damage (int) - The amount of damage to take
    def take_damage(self, damage):

        self._health -= damage

        # If health is less than zero, set to zero
        if(self._health < 0):
            self._health = 0

        # Refresh GUI if applicable
        self.gui_refresh()

    # - attack()
    # Attack another character
    #
    # self
    # enemy (Character) - The character to attack
    def attack(self, enemy):

        # Calculate attack damage to do
        # Check that this character has a weapon to use
        if(self._weapon != None):
            # Get weapon attack damage value
            attack_dam = self._weapon.attack_damage()
            # Check if the enemy has armour
            if(enemy.armour() != None):
                # Subtract protection value from attack value
                attack_dam -= enemy.armour().protection()
                # Check if value is negative
                if(attack_dam < 0):
                    # Attack damage is negative, set to zero
                    attack_dam = 0
        else:
            # No weapon, set damage to zero
            attack_dam = 0

        # Apply damage to enemy
        enemy.take_damage(attack_dam)

        # Refresh GUI if applicable
        self.gui_refresh()

        # Return the attack damage
        return(attack_dam)

    # - gui()
    # Creates a gui object associated with the character
    #
    # self
    # parent (tkinter) - The parent tkinter object
    def gui(self, parent):
        
        # Create parent GUI object
        self._gui = tk.Frame(parent)
        self._gui.pack(fill = tk.X)

        # Set character name label
        tk.Label(self._gui, text = self._name, anchor = tk.W).pack(fill = tk.X)

        # Setup health, weapon, and armour label
        self._health_label = tk.Label(self._gui, anchor = tk.W)
        self._weapon_label = tk.Label(self._gui, anchor = tk.W)
        self._armour_label = tk.Label(self._gui, anchor = tk.W)
        # Pack them
        self._health_label.pack(fill = tk.X)
        self._weapon_label.pack(fill = tk.X)
        self._armour_label.pack(fill = tk.X)

        # Refresh GUI
        self.gui_refresh()
        
    # - gui_refresh()
    # Update text variable with new values
    #
    # self
    def gui_refresh(self):

        # Check for gui
        if(self._gui != None):

            # Set labels
            self._health_label.config(text = f"Health: {self._health}")
            # Check if weapon exists
            if(self._weapon != None):
                self._weapon_label.config(text = f"Weapon: {self._weapon.name()}")
            else:
                self._weapon_label.config(text = "Weapon: None")
            # Check if armour exists
            if(self._armour != None):
                self._armour_label.config(text = f"Armour: {self._armour.name()}")
            else:
                self._armour_label.config(text = "Armour: None")

# - Player
# Child of Character
class Player(Character):

    # - __init__()
    #
    # self
    # name (str) - The name of player
    # weapon (items.Weapon) - The weapon the player starts with
    # armour (items.Armour) - The armour the player starts with
    # game_map (rooms.Map) - The map of rooms the player can explore
    def __init__(self, name, game_map, weapon = items.Weapon("Stick", 1, 4), armour = None):

        # Set attributes
        self._map = game_map
        self._room = self._map.start_room()
        self._position = self._room.find_entrance("m")

        # Set attributes associated with Character object
        super().__init__(name, weapon = weapon, armour = armour)

        # Replace inventory object with one that will pass to self.use function
        self._inventory = items.Inventory(self.use)

    # - room()
    # Return current room
    #
    # self
    def room(self):

        return(self._room)

    # - position()
    # Return player position
    # 
    # self
    def position(self):

        return(self._position)    

    # - inventory()
    # Return player inventory object
    # 
    # self
    def inventory(self):

        return(self._inventory)    

    # - use()
    # Defines how to use an item
    #
    # self
    # item (items.Item) -  The item to be "used"
    def use(self, item):

        # Check item type to determine action

        if(type(item) == items.Weapon):
            # If the item is a weapon
            # Check if a weapon is equipped by the player
            if(self._weapon != None):
                # If it is then add it the inventory
                self._inventory.add_item(self._weapon)
            # Put the new weapon into the slot
            self._weapon = item
        elif(type(item) == items.Armour):
            # If item is a piece of armour
            # Check if armour is equipped by the player
            if(self._armour != None):
                # If it is then add it to the inventory
                self._inventory.add_item(self._armour)
            # Equip the new piece of armour
            self._armour = item
        elif(type(item) == items.Potion):
            # If the item is a potion
            # Add the health effect to our health
            self._health += item.health_effect()
        elif(type(item) == items.Key):
            # If the item is a key, use it
            item.use()

        # Refresh GUI if applicable
        self.gui_refresh()

    # - move()
    # Move the player by an amount x/y in the room
    #
    # self
    # row (int): The amount to move the player in x
    # column (int): The amount to move the player in y
    def move(self, row, column):

        # Calculate the new row and colum
        new_row = self._position[0] + row
        new_column = self._position[1] - column

        # Get room grid and feed in new x and y vals
        try:
            grid_value = self._room.grid()[new_row][new_column]
        except(IndexError):
            # Tried to access an area outside of the grid
            self.move(0, 0) # Checking no move in case this is a door
            return

        # If the move makes a negative Index
        if((new_row < 0) or (new_column < 0)):
            # Tried to access an area outside of the grid
            self.move(0, 0) # Checking no move in case this is a door
            return

        if((grid_value == 0) or (grid_value == "m")):
            # If grid value is zero or m, not wall, thus move
            self._position[0] = new_row
            self._position[1] = new_column      
        elif(type(grid_value) == rooms.Room):
            # If the grid value is a room object then we are jumping rooms
            self.change_room(grid_value, "m")
        elif(type(grid_value) == str):
            # Grid value is string (that is not m) so must be at entrance, we need to move rooms
            if(grid_value == "n"):
                # Set room to be north of current room
                self.change_room(self._room.north_of(), "s")
            elif(grid_value == "e"):
                # Set room to be east of current room
                self.change_room(self._room.east_of(), "w")
            elif(grid_value == "s"):
                # Set room to be south of current room
                self.change_room(self._room.south_of(), "n")
            elif(grid_value == "w"):
                # Set room to be west of current room
                self.change_room(self._room.west_of(), "e")
        # Else it's a wall, do not move

    # - change_room()
    # Change the room the player is in
    #
    # self
    # room (rooms.Room): The room the player is to move to
    # entrance (str): The name of the entrance the player will appear in e.g. "n"
    def change_room(self, room, entrance):
        
        # Set current room to new room
        new_position = room.find_entrance(entrance)
        # Make sure the new room and entrance really exist first
        if(new_position != False):
            self._room = room
            self._position = new_position
            
# - Enemy
# Child of Character
class Enemy(Character):

    # Currently don't need code in here 
    pass

# - Main
# Used for testing code associated with this module so this code should only run when it is main
if(__name__ == "__main__"):

    # Tkinter setup
    root = tk.Tk()
    root.geometry("300x100+100+100")

    start_room = rooms.Room("The Entrance", n = True)
    end_room = rooms.Room("The Bee Room", s = True, n = start_room)

    # Initialise a map
    game_map = rooms.Map([[start_room], [end_room]], start_room, end_room)

    # Create player object
    player = Player("Jordan Hay", game_map)
    player.inventory().add_items([
            items.Item("Bees"),
            items.Weapon("A HIVE FULL OF BEES", 10, 300),
            items.Armour("Honeycomb Kneepads", 100),
            items.Potion("10mL Syringe full of Honey", 10)
        ])

    # Display player inventory
    #player.inventory().gui(root)

    # Display player stats
    player.gui(root)

    # Root mainloop
    root.mainloop()
    
