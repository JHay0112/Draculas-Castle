'''

    characters.py

    Author: Jordan Hay
    Date: 2020-09-07

    Characters, e.g. the player, enemies, in Dracula's Castle

'''

# - Imports

import items # Create items
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
    def __init__(self, name, weapon = items.Weapon("Stick", [10, 20]), armour = None):

        # Set attributes
        self._room = None # Room the player is in
        self._position = [0, 0] # Position of the player in room [x, y]

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
    
