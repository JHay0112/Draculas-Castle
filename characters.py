'''

    characters.py

    Author: Jordan Hay
    Date: 2020-09-07

    Characters, e.g. the player, enemies, in Dracula's Castle

'''

# - Imports

import items # Create items

# - Classes

# The player object
class Player:

    # - __init__()
    #
    # self
    # name (str) - The name of player
    # weapon (items.Weapon) - The weapon the player starts with
    # armour (items.Armour) - The armour the player starts with
    def __init__(self, name, weapon = items.Weapon("Stick", [10, 20]), armour = None):

        # Set attributes
        self._name = name
        self.Inventory(self.use) 
        self._weapon = weapon
        self._armour = armour
        self._health = 100
        self._room = None # Room the player is in
        self._position = [0, 0] # Position of the player in room [x, y]

    # - weapon()
    # Returns the weapon object the player uses
    #
    # self
    def weapon(self):

        return(self._weapon)

    # - use()
    # Defines how to use an item
    #
    # self
    # item (items.Item) -  The item to be "used"
    def use(self, item):

        # Can do this later

        # Would check for item type
        # "Using" a Weapon or Armour would equip them
        # Potion would apply the effect to the player
        
        pass

# The enemy object
class Enemy:

    # - __init__()
    #
    # self
    # name (str) - The name of the enemy
    # health (int) - The health of the enemy
    # weapon (items.Weapon) - The weapon the enemy uses
    # armour (items.Armour) - The armour the enemy uses
    def __init__(self, name, health, weapon, armour):

        # Set attributes
        self._name = name
        self.Inventory() 
        self._weapon = weapon
        self._armour = armour
        self._health = health

    # - weapon()
    # Returns the weapon object the enemy uses
    #
    # self
    def weapon(self):

        return(self._weapon)
