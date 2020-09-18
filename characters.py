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
    def __init__(self, name, health = 100, weapon = None, armour = None):

        self._name = name
        self._inventory = items.Inventory() 
        self._weapon = weapon
        self._armour = armour
        self._health = health

    # - weapon()
    # Returns the weapon object the enemy uses
    #
    # self
    def weapon(self):

        return(self._weapon)

    # - inventory()
    # Returns the inventory object of the character
    #
    # self
    def inventory(self):

        return(self._inventory)

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
    def __init__(self, name, weapon = items.Weapon("Stick", [10, 20]), armour = None, game_map = None):

        # Set attributes
        self._map = game_map
        self._room = self._map.start_room() # Room the player is in
        self._position = [-1, 3] # Position of the player in room [x, y]

        # Set attributes associated with Character
        super().__init__(name, weapon = weapon, armour = armour)

        # Replace inventory object with one that will pass to self.use function
        self._inventory = items.Inventory(self.use)

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
                self._inventory.add_item(self._weapon)
            # Equip the new piece of armour
            self._armour = item
        elif(type(item) == items.Potion):
            # If the item is a potion
            # Add the health effect to our health
            self._health += item.health_effect()

    # - room_obj()
    # object representation of current room
    def room_obj(self):

        return(self._map.find_room(self._room))

    # - move()
    # Move the player by an amount x/y in the room
    #
    # self
    # x (int): The amount to move the player in x
    # y (int): The amount to move the player in y
    def move(self, x, y):

        # Calculate the new x and y
        new_x = self._position[0] += x
        new_y = self._position[1] += y

        # Get room grid and feed in new x and y vals
        grid_value = self.room_obj().grid()[new_x, new_y]

        # If the grid value is a string
        if(type(grid_value) == str):
            # Grid value is string so must be at entrance, we need to move rooms
            if(grid_value = "n"):
                # Move room position one north
                self._room[1] += 1
                # Update position to be new room southern entrance
                self._position = self.room_obj().find_entrance("s")
            elif(grid_value = "e"):
                # Move room position east
                self._room[0] += 1
                # Update position to be new room west entrance
                self._position = self.room_obj().find_entrance("w")
            elif(grid_value = "s"):
                # Move room position south
                self._room[1] -= 1
                # Update position to be new room north entrance
                self._position = self.room_obj().find_entrance("n")
            elif(grid_value = "w"):
                # Move room position west
                self._room[0] -= 1
                # Update position to be new room east entrance
                self._position = self.room_obj().find_entrance("e")
        elif(grid_value == 0):
            # If grid value is zero, not wall, thus move
            self._position[0] += x
            self._position[1] += y
        # Else it's a wall, do not move

    # - change_room()
    # Change the room the player is in
    #
    # self
    # room (list): The room the player is to move to
    # entrance (str): The name of the entrance the player will appear in e.g. "n"
    def change_room(self, room, entrance):

        # Flag for if room is locked
        locked = True
        room_obj = self._map.find_room(room) # Get object represenation of room

        # Check if room is locked
        if(type(room_obj.key()) == items.Key):
            # If room is locked check the player inventory for the relevant key
            if(room_obj.key() in self._inventory.items()):
                # If the player has the key then unlock the room
                locked = False
            # Else rooms stays locked, nothing changes
        else:
            # Room is not locked, so set it as not locked
            locked = False

        if(not locked):
            # Set current room to new room
            self._room = room
            self._position = room.find_entrance(entrance)
            

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

    # Create player object
    player = Player("Jordan Hay")
    player.inventory().add_items([
            items.Item("Bees"),
            items.Weapon("A HIVE FULL OF BEES", [10, 300]),
            items.Armour("Honeycomb Kneepads", 100),
            items.Potion("10mL Syringe full of Honey", 10)
        ])

    # Display player inventory
    player.inventory().gui(root)
    
