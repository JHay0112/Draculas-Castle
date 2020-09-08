'''

    items.py

    Author: Jordan Hay
    Date: 2020-09-06

    Item/inventory objects for Dracula's Castle

'''

# - Imports

# - Classes

# The base Item class
class Item:

    # - __init__()
    # Initialise Item Object
    #
    # self
    # name (str) - The name of the item
    def __init__(self, name):

        # Set item attributes
        self._name = name

# Weapon class, child of Item
class Weapon(Item):

    # - __init__()
    # Initialise Weapon Object
    #
    # self
    # name (str) - The name of the weapon
    # attack_damage (int) - The damage the weapon does
    def __init__(self, name, attack_damage):

        # Set weapon attributes
        self._attack_damage = attack_damage

        # Set attributes associated with parent item
        super().__init__(name)

# Inventory class, used for item management
class Inventory:

    pass
