'''

    characters.py

    Author: Jordan Hay
    Date: 2020-09-07

    Characters, e.g. the player, enemies, in Dracula's Castle

'''

# - Imports

import items # Create items

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

# - Enemy
# Child of Character
class Enemy(Character):

    # Currently don't need code in here 
    pass
