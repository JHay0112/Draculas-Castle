'''

    map.py

    Author: Jordan Hay
    Date: 2020-09-06

    Map and rooms for Dracula's Castle.

'''

# - Imports

import tkinter as tk # GUI
from tkinter import ttk # Refined GUI elements
import items # Item management

# - Classes

# - Map
# Arranges and controls a set of room objects
# Version: 1.1
class Map:

    # - __init__()
    # Initialise a map object
    #
    # self
    # map (2D list) - 2d list of room locations in map
    # start_room (Room) - The room in which the player starts in the map
    # boss_room (Room) - The final room in which the player does battle with the final boss
    def __init__(self, map, start_room, boss_room):

        self._map = map
        self._start_room = start_room
        self._boss_room = boss_room

    # - start_room()
    # Returns the room object that the player starts in
    #
    # self
    def start_room(self):

        return(self._start_room)

    # - boss_room()
    # Returns the room object the player ends in
    #
    # self
    def boss_room(self):

        return(self._start_room)

# - Room
# Holds attributes of a room, e.g. entrances, inventory
# Version: 0.1
class Room:

    # - __init__()
    # Initialise a room object
    # 
    # self
    # name (str) - Name of the room
    # n (bool/Room) -  
    # key (str) - The name of the key the room requires to unlock, default None
    def __init__(self, name, n = False, s = False, e = False, w = False, key = None):

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
        self._grid = [
            [0, 0, self._n, "n", self._n, 0, 0],
            [0, 1, 1, not self._n, 1, 1, 0],
            [self._w, 1, 0, 0, 0, 1, self._e],
            ["w", not self._w, 0, 0, 0, not self._e, "e"],
            [self._w, 1, 0, 0, 0, 1, self._e],
            [0, 1, 1, not self._s, 1, 1, 0,],
            [0, 0, self._s, "s", self._s, 0, 0]
        ] # Grid represenation of this specific room with entrances added

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
    # parent
    def gui(self, parent, height, width):

        # Initialise the canvas object
        self._gui = tk.Canvas(parent, height = height, width = width)
        self._gui.pack(fill = tk.BOTH)

        rows = len(self._grid) # Rows in grid
        grid_height = height/rows # Calculate the height of each grid piece

        # Iteration counters
        row_num = 0
        column_num = 0

        # For every row
        for row in self._grid:

            # Start at zeroeth column
            column_num = 0
            columns = len(row) # Get columns in row
            grid_width = width/columns # Calculate the width of each grid piece

            # For every column in this row
            for column in row:

                # If the column is non-zero and non-string
                if((column != 0) and (type(column) != str)):

                    fill = "black"

                    # Calculate coordinates
                    x0 = column_num * grid_width
                    y0 = row_num * grid_height
                    x1 = x0 + grid_width
                    y1 = y0 + grid_height

                    # Generate rectangle
                    self._gui.create_rectangle(x0, y0, x1, y1, fill = fill, outline = "")

                # Iterate column
                column_num += 1

            # Iterate row
            row_num += 1

# - Main
# Used for testing code associated with this module so this code should only run when it is main
if(__name__ == "__main__"):

    # Tkinter setup
    root = tk.Tk()
    root.geometry("300x300+100+100")

    # Create Room object
    room = Room("Test Chamber #1", n = True, e = True)
    room.gui(root, 300, 300)

    # Root mainloop
    root.mainloop()
