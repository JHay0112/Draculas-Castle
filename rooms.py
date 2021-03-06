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

    # Constants
    HEIGHT = 400
    WIDTH = 400

    # - __init__()
    # Initialise a room object
    # 
    # self
    # name (str) - Name of the room
    # n, s, e, w (bool/Room) - Stores
    def __init__(self, name, n = False, s = False, e = False, w = False):

        # Set Room attributes
        self._name = name # Name of the room
        # Defining what entrances are there
        self._entrances = {
                "n": n,
                "s": s,
                "e": e,
                "w": w
            }
        self._gui = None # Stores GUI object associated with room
        self._map = None # Map object associated with the room, set when Map object is initialised
        self._map_key = None # Where in the grid representation of the map the room is found, set by Map object
        self._inventory = items.Inventory(use_name = "PICK UP") # Room inventory
        self._player = None # The player's canvas object
        self._enemies = [] # Enemies in the room
        self._grid = [] # Grid represenation of this specific room with entrances added

        self.check_entrances()

    # - check_entrances()
    # Checks if entrances are linked to specific rooms
    #
    # self
    def check_entrances(self):

        # Refresh grid
        self.grid_refresh()

        for entrance_name, entrance_value in self._entrances.items():
            # If a room object is stored in the entrance_var
            if(type(entrance_value) == Room):
                # Find the entrance key
                map_key = self.find_entrance(entrance_name)
                # Insert the object into the map
                self._grid[map_key[0]][map_key[1]] = entrance_value

    # - grid_refresh()
    # Refresh the grid
    #
    # self
    def grid_refresh(self):

        # Compute grid
        self._grid = [
                [0, 0, self._entrances["n"], "n", self._entrances["n"], 0, 0],
                [0, 1, 1, not self._entrances["n"], 1, 1, 0],
                [self._entrances["w"], 1, 0, 0, 0, 1, self._entrances["e"]],
                ["w", not self._entrances["w"], 0, "m", 0, not self._entrances["e"], "e"],
                [self._entrances["w"], 1, 0, 0, 0, 1, self._entrances["e"]],
                [0, 1, 1, not self._entrances["s"], 1, 1, 0,],
                [0, 0, self._entrances["s"], "s", self._entrances["s"], 0, 0]
            ] # Grid represenation of this specific room with entrances added

    # - add_entrance()
    # Changes an entrance value
    #
    # self
    # entrance_name (str) - The name of the entrance to modify
    # new_val (bool/Room) - The new value to insert
    def add_entrance(self, entrance_name, new_val):

        # Set the new value
        self._entrances[entrance_name] = new_val
        # Check all entrances
        self.check_entrances()

    # - entrances()
    # Returns dict of entrances
    #
    # self
    def entrances(self):

        return(self._entrances)

    # - grid()
    # Returns the room's grid
    #
    # self
    def grid(self):

        return(self._grid)

    # - inventory()
    # Returns the room's inventory object
    #
    # self
    def inventory(self):

        return(self._inventory)

    # - enemies()
    # Returns list of enemies in the room
    # 
    # self
    def enemies(self):

        return(self._enemies)

    # - add_enemy()
    # Add enemy to list of enemies
    # 
    # self
    # enemy (characters.Enemy) - The enemy to add
    def add_enemy(self, enemy):

        self._enemies.append(enemy)

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

        # Iteration counters
        row_num = 0
        column_num = 0

        # For every row
        for row in self._grid:

            # Start at column zero
            column_num = 0

            # For every column in row
            for column in row:

                # if column is the same as the entrance string
                if(column == entrance):
                    # Then return the position
                    return([row_num, column_num])

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

        # Row up, same column
        return(self._map.grid()[self._map_key[0] - 1][self._map_key[1]])

    # - south_of()
    # Returns the room sooth of this room
    #
    # self
    def south_of(self):

        # Row down, same column
        return(self._map.grid()[self._map_key[0] + 1][self._map_key[1]])

    # - east_of()
    # Returns the room north of this room
    #
    # self
    def east_of(self):

        # Column right, same row
        return(self._map.grid()[self._map_key[0]][self._map_key[1] + 1])

    # - west_of()
    # Returns the room north of this room
    #
    # self
    def west_of(self):

        # Column left, same row
        return(self._map.grid()[self._map_key[0]][self._map_key[1] - 1])

    # - middle()
    # Returns the coordinates of the centre of the room
    #
    # self
    def middle(self):

        return([round(len(self._grid[0]) / 2), round(len(self._grid) / 2)])

    # - gui()
    # Creates the gui object
    #
    # self
    # parent (tkinter)
    # height (int)
    # width (int)
    def gui(self, parent):

        height = Room.HEIGHT
        width = Room.WIDTH

        # Initialise the canvas object
        self._gui = tk.Canvas(parent, height = height, width = width, bg = "grey")
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
                if((column != 0) and (type(column) != str) and (type(column) != Room)):

                    # Calculate coordinates
                    x0 = column_num * grid_width
                    y0 = row_num * grid_height
                    x1 = x0 + grid_width
                    y1 = y0 + grid_height

                    # Generate rectangle
                    self._gui.create_rectangle(x0, y0, x1, y1, fill = "black", outline = "")

                # Iterate column
                column_num += 1

            # Iterate row
            row_num += 1

        # Add room name to canvas
        self._gui.create_text(width/2, height/2, text = self._name, fill = "white")

    # - draw_player()
    # Draw's the player onto the map
    #
    # self
    # player (characters.Player): The player object to draw
    def draw_player(self, player):

        rows = len(self._grid) # Rows in grid
        grid_height = Room.HEIGHT/rows # Calculate the height of each grid piece
        columns = len(self._grid[0]) # Get columns in first row
        grid_width = Room.WIDTH/columns # Calculate the width of each grid piece

        # Check if player has already been draw
        if(self._player != None):
            # If so, remove it
            self._gui.delete(self._player)
            self._player = None

        # Get player position
        position = player.position()
        
        # Calculate coordinates
        x0 = position[1] * grid_width
        y0 = position[0] * grid_height
        x1 = x0 + grid_width
        y1 = y0 + grid_height

        # Generate rectangle
        self._player = self._gui.create_rectangle(x0, y0, x1, y1, fill = "maroon", outline = "")
        # Lower player below text
        self._gui.tag_lower(self._player)


# - Main
# Used for testing code associated with this module so this code should only run when it is main
if(__name__ == "__main__"):

    # Tkinter setup
    root = tk.Tk()
    root.geometry("300x300+100+100")

    # Create Room object
    room = Room("Test Chamber #1", n = True, e = True)
    room2 = Room("Not the Test Chamber", w = room)

    room2.gui(root)

    # Root mainloop
    root.mainloop()
