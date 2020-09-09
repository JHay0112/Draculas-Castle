'''

    map.py

    Author: Jordan Hay
    Date: 2020-09-06

    Map and rooms for Dracula's Castle.

'''

# - Imports

import items # Item management

# - Classes

# Map for organising rooms
class Map:

    # - __init__()
    # Initialise a map object
    #
    # self
    # map (2D list) - 2d list of room locations in map
    def __init__(self, map):

        self._map = map

# Rooms in a map
class Room:

    # - __init__()
    # Initialise a room object
    # 
    # self
    # name (str) - Name of the room
    # n (bool/Room) -  
    # key (str) - The name of the key the room requires to unlock, default None
    def __init__(self, name, n = None, s = None, e = None, w = None, key = None):

        # Set Room attributes
        self._name = name
        self._n = n
        self._s = s
        self._e = e 
        self._w = w 
        self._key = key
        self._gui = None
        self._inventory = items.Inventory()
        self._enemies = []

    # - key()
    # Returns the key value
    #
    # self
    def key(self):
        
        return(self._key)

    # - gui()
    # Returns the gui object
    #
    # self
    def gui(self):

        pass