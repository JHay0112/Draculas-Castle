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
    # damage (list [min, max]) - The min and max damage
    def __init__(self, name, damage):

        # Set weapon attributes
        self._damage = damage

        # Set attributes associated with parent item
        super().__init__(name)

# Armour class, child of item
class Armour(Item):

    # - __init__()
    # Initialise Armour Object
    #
    # self
    # name (str) - The name of the armour
    # protection (int) - Amount of damage the armour will protect from
    def __init__(self, name, protection):

        # Set armour attributes
        self._protection = protection

        # Set attributes associated with parent item
        super().__init__(name)

# Potion class, child of Item
class Potion(Item):

    # - __init__()
    # Initialise Potion Object
    #
    # self
    # name (str) - The name of the potion
    # health_effect (init) - Amount of health the item will give the user
    def __init__(self, name, health_effect):

        # Set armour attributes
        self._health_effect = health_effect

        # Set attributes associated with parent item
        super().__init__(name)

# Inventory class, used for item management
class Inventory:

    pass
