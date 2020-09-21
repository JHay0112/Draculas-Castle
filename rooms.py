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
    # start_room (list) - The position of the room in which the player starts in the map
    # boss_room (list) - The position of the final room in which the player does battle with the final boss
    def __init__(self, game_map, start_room, boss_room):

        self._map = game_map
        self._start_room = start_room
        self._boss_room = boss_room

        # Row iteration counter
        row_num = 0

        # Set map values in room objects
        # For each row
        for row in self._map:

            # Column iteration counter
            column_num = 0

            # For each room/column in the row
            for column in row:
                # Set the map, passing self and row/column coords
                column.set_map(self, [row_num, column_num])

                # Iterate column num
                column_num += 1

            # Iterate row num
            row_num += 1

    # - grid()
    # Returns the map grid representation
    #
    # self
    def grid(self):

        return(self._map)

    # - start_room()
    # Returns the room position that the player starts in
    #
    # self
    def start_room(self):

        return(self._start_room)

    # - boss_room()
    # Returns the room position the player ends in
    #
    # self
    def boss_room(self):

        return(self._boss_room)

# - Room
# Holds attributes of a room, e.g. entrances, inventory
# Version: 0.1
class Room:

    # - __init__()
    # Initialise a room object
    # 
    # self
    # name (str) - Name of the room
    # n, s, e, w (bool/Room) -  Stores
    # key (str) - The name of the key the room requires to unlock, default None
    def __init__(self, name, n = False, s = False, e = False, w = False, key = None):

        # Set Room attributes
        self._name = name # Name of the room
        # Defining what entrances are there
        self._n = n
        self._s = s
        self._e = e 
        self._w = w 
        self._key = key # If the room requires a key
        self._gui = None # Stores GUI object associated with room
        self._map = None # Map object associated with the room, set when Map object is initialised
        self._map_key = None # Where in the grid representation of the map the room is found, set by Map object
        self._inventory = items.Inventory() # Room inventory
        self._enemies = [] # Enemies in the room
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

    # - grid()
    # Returns the room's grid
    #
    # self
    def grid(self):

        return(self._grid)

    # - set_map()
    # Sets the map the room is in
    #
    # self
    # game_map (Map) - The map the room can be found in
    # map_key ([row, column]) - The key value that returns the room in the map
    def set_map(self, game_map, map_key):

        self._map = game_map
        self._map_key = map_key

    # - find_entrance()
    # Returns the position of a selected entrance
    #
    # self
    # entrance (str): Name of the entrance to find
    def find_entrance(self, entrance):

        rows = len(self._grid) # Rows in grid

        # Iteration counters
        row_num = 0
        column_num = 0

        # For every row
        for row in self._grid:

            # Start at column zero
            column_num = 0
            columns = len(row) # Get columns in row

            # For every column in row
            for column in row:

                # if column is the same as the entrance string
                if(column == entrance):
                    # Then return the position
                    return([column_num, row_num])

                # Iterate column num
                column_num += 1

            # Iterate row num
            row_num += 1

        # If we get to this point then there is no entrance return false
        return(False)

    # - north_of()
    # Returns the room north of this room
    #
    # self
    def north_of(self):

        return(self._map.grid()[self._key[0]][self._key[1] - 1])

    # - south_of()
    # Returns the room sooth of this room
    #
    # self
    def south_of(self):

        return(self._map.grid()[self._key[0]][self._key[1] + 1])

    # - east_of()
    # Returns the room north of this room
    #
    # self
    def east_of(self):

        return(self._map.grid()[self._key[0] + 1][self._key[1]])

    # - west_of()
    # Returns the room north of this room
    #
    # self
    def west_of(self):

        return(self._map.grid()[self._key[0] - 1][self._key[1]])

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
