'''

    items.py

    Author: Jordan Hay
    Date: 2020-09-06

    Item/inventory objects for Dracula's Castle

'''

# - Imports

import random # Produce pseudo-random results

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

    # - attack()
    # Returns attack damage
    #
    # self
    def attack_damage(self):

        # Get max and min damage values
        min_damage = self._damage[0]
        max_damage = self._damage[1]

        # Get random value between max and min damage
        damage = random.randint(min_damage, max_damage)

        return(damage)

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

    # - defend()
    # Returns amount of damage to be protected, random between no protection and all set protection
    #
    # self
    def protection(self):

        # Get random value between zero and protection
        protection = random.randint(0, self._protection)

        return(protection)

# Potion class, child of Item
class Potion(Item):

    # - __init__()
    # Initialise Potion Object
    #
    # self
    # name (str) - The name of the potion
    # health_effect (init) - Amount of health the item will give the user
    def __init__(self, name, health_effect):

        # Set potion attributes
        self._health_effect = health_effect

        # Set attributes associated with parent item
        super().__init__(name)

    # - health_effect()
    # Get the amount of health this potion will effect
    #
    # self
    def health_effect(self):

        return(self._health_effect)

# Key class, child of Item
class Key(Item):

    # - __init__()
    # Initialise Key Object
    #
    # self
    # name (str) - The name of the key
    def __init__(self, name):

        # Set attributes associated with parent item
        super().__init__(name)

# Inventory class, used for item management
class Inventory:

    pass
