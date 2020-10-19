'''

    items.py

    Author: Jordan Hay
    Date: 2020-09-06

    Item/inventory objects for Dracula's Castle

'''

# - Imports

import random # Produce pseudo-random results
import tkinter as tk # GUI
from tkinter import ttk # Refined GUI elements

# - Classes

# The base Item class
class Item:

    # - __init__()
    # Initialise Item Object
    #
    # self
    # name (str) - The name of the item
    def __init__(self, name, useable = False):

        # Set item attributes
        self._name = name
        self._useable = useable

    # - name()
    # Returns the name of the object
    #
    # self
    def name(self):
        return(self._name)

    # - useable()
    # Returns whether the item is usable or not
    #
    # self
    def useable(self):
        return(self._useable)

    # - set_useable()
    # Sets the usability of an item
    #
    # self
    # state (bool) - The state to set the flag to
    def set_useable(self, state):

        self._useable = state

# Weapon class, child of Item
class Weapon(Item):

    # - __init__()
    # Initialise Weapon Object
    #
    # self
    # name (str) - The name of the weapon
    # damage (list [min, max]) - The min and max damage
    def __init__(self, name, min_dam, max_dam):

        # Set weapon attributes
        self._min_damage = min_dam
        self._max_damage = max_dam

        # Set attributes associated with parent item
        super().__init__(name, True)

    # - attack()
    # Returns attack damage
    #
    # self
    def attack_damage(self):

        # Get random value between max and min damage
        damage = random.randint(self._min_damage, self._max_damage)

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
        super().__init__(name, True)

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
        super().__init__(name, True)

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
    # callback (function) - The function to call when the key is used
    def __init__(self, name, callback = None):

        # Store callback function
        self._callback = callback

        # Set attributes associated with parent item
        super().__init__(name, True)

    # - use()
    # use the key
    #
    # self
    def use(self):

        # Check if callback exists first
        if(self._callback != None):
            self._callback()

    # - set_callback()
    # Set the callback function
    #
    # self
    # callback (function) - The function call on use
    def set_callback(self, callback):

        self._callback = callback

# Inventory class, used for item management
class Inventory:

    # - __init__()
    #  Initialise Inventory Object
    #
    # self
    # use_command (Function) - The function to run when an item is used
    # use_name (str) - The name of the button associated with the use command
    def __init__(self, use_command = None, use_name = "USE"):

        # Set inventory attributes
        self._items = [] # List of item objects stored by inventory
        self._use_command = use_command
        self._use_name = use_name
        self._gui = None # Store GUI object (Frame)
        self._position = 0 # Store where in the list of items the GUI is viewing

    # - set_use_command()
    # Set the use command associated with the inventory
    #
    # self
    # use_command (Function) - the function to run when an item is used
    def set_use_command(self, use_command):

        self._use_command = use_command
        
    # - gui()
    # Initialise a GUI object in the inventory
    #
    # self
    # parent (Tkinter) - The parent frame/root object the gui is displayed in
    def gui(self, parent):

        # Button width, spent some time weaking this so figured it was best a constant
        BUTTON_WIDTH = 7

        # Create frame to hold items and pack it
        self._gui = tk.Frame(parent, height = 100, width = 200)
        self._gui.pack_propagate(False)
        self._gui.pack(fill = tk.BOTH)

        # Create a frame for the item to be displayed in
        self._item_frame = tk.Frame(self._gui, height = 60)
        self._item_frame.pack_propagate(False)
        self._item_frame.pack(fill = tk.X,
                              ipadx = 5,
                              ipady = 5)

        # Create a frame for the controls to be displayed in
        self._control_frame = tk.Frame(self._gui)
        self._control_frame.pack(fill = tk.X)

        # Add the control buttons to the control frame
        # Up button
        self._up_button = ttk.Button(self._control_frame,
                                     text = "↑",
                                     state = tk.DISABLED,
                                     command = self.gui_up,
                                     width = BUTTON_WIDTH)
        self._up_button.pack(side = tk.LEFT, expand = True)

        # Down button
        self._down_button = ttk.Button(self._control_frame,
                                       text = "↓",
                                       state = tk.DISABLED,
                                       command = self.gui_down,
                                       width = BUTTON_WIDTH)
        self._down_button.pack(side = tk.LEFT, expand = True)

        # Use button
        self._use_button = ttk.Button(self._control_frame,
                                      text = self._use_name,
                                      state = tk.DISABLED,
                                      command = self.use,
                                      width = BUTTON_WIDTH)
        self._use_button.pack(side = tk.LEFT, expand = True)

        # Discard button
        self._drop_button = ttk.Button(self._control_frame,
                                       text = "DROP",
                                       state = tk.DISABLED,
                                       width = BUTTON_WIDTH)
        self._drop_button.pack(side = tk.LEFT, expand = True)

        # Refresh the GUI
        self.gui_refresh()

    # - gui_refresh()
    # Refreshes what the gui representation of this inventory is
    #
    # self
    def gui_refresh(self):

        # First check that a GUI exists, if it doesn't then we can skip all this code
        if(self._gui is not None):

            # Remove all widgets in the item frame
            for widget in self._item_frame.winfo_children():
                widget.destroy()

            # Check that there are items in the Inventory
            if(self._items == []):

                # There are no items so we will tell the user this
                tk.Label(self._item_frame, text = "Inventory is Empty!").pack(pady = 20)
                # Check and set the button states for no item
                self.check_buttons(None)

            else:
                # The list is not empty so lets display an item

                # Try and get the item at the specified position
                try:
                    current_item = self._items[self._position]
                except:
                    # If we can't get the specified position we will get the item at position zero
                    # Since the list isn't empty, we've already checked that, we know there will be an item at zero
                    # An alternative would to be move up one position and recurse, this could cause lag if the position is way off though
                    current_item = self._items[0]

                # Check and set the button states
                self.check_buttons(current_item)

                # Display item info
                tk.Label(self._item_frame, text = current_item.name()).pack(anchor = tk.W, pady = (10, 0))
                tk.Label(self._item_frame, text = type(current_item).__name__).pack(anchor = tk.W)

    # - check_buttons()
    # Checks and sets the states of the control buttons
    #
    # self
    # item (Item) - The item that we are checking the states of the buttons relative to
    def check_buttons(self, item):

        # Check the item exists
        if(item is not None):
            # If it exists we can discard it
            self._drop_button.config(state = tk.ACTIVE)
            self._drop_button.config(command = lambda i = item: self.drop_item(i))

            # If the current position is zero then disable the up button
            if(self._position == 0):
                self._up_button.config(state = tk.DISABLED)
            else:
                self._up_button.config(state = tk.ACTIVE)

            # If the current position is greater or equal to the length of list of items then disable the down button
            if(self._position >= len(self._items) - 1):
                self._down_button.config(state = tk.DISABLED)
            else:
                self._down_button.config(state = tk.ACTIVE)

            # If the current item is useable then use it
    
            if(item.useable() == False):
                self._use_button.config(state = tk.DISABLED)
            else:
                self._use_button.config(state = tk.ACTIVE)
        else:
            # Item does not exist we cannot do anything with it, and the inventory must be empty
            self._drop_button.config(state = tk.DISABLED)
            self._up_button.config(state = tk.DISABLED)
            self._down_button.config(state = tk.DISABLED)
            self._use_button.config(state = tk.DISABLED)

    # - gui_up()
    # Moves the GUI's position in the list up
    #
    # self
    def gui_up(self):

        self._position -= 1
        self.gui_refresh()

    # - gui_down()
    # Moves the GUI's position in the list down
    #
    # self
    def gui_down(self):

        self._position += 1
        self.gui_refresh()

    # - items()
    # Return a list of the items in the inventory
    #
    # self
    def items(self):

        return(self._items)

    # - add_item()
    # Add item to the inventory
    #
    # self
    # new_item (Item) - A new item object to store in the inventory
    def add_item(self, new_item):

        # Append the new item
        self._items.append(new_item)
        # Refresh the GUI if applicable
        self.gui_refresh()

    # - add_items()
    # Add multiple items to the inventory
    # 
    # self
    # new_items (list of Items) - List of items to add to the inventory
    def add_items(self, new_items):

        # For every item in the list
        for item in new_items:
            # Add the item to the inventory
            self.add_item(item)

        # Refresh the GUI if applicable
        self.gui_refresh()

    # - drop_item()
    # Remove the item from the inventory
    # 
    # self
    # item (Item) - The item to be removed from the inventory
    def drop_item(self, item):

        # Drop the item from the list
        self._items.remove(item)
        # Refresh the GUI if applicable
        self.gui_refresh()

    # - drop_all()
    # Removes all items in inventory
    #
    # self
    def drop_all(self):

        # Set items to empty list
        self._items = []

    # - use()
    # Uses the current item if a use command is set
    #
    # self
    def use(self):

        # Get current item
        item = self._items[self._position]

        # If there is a use command then run it with the item as an argument
        if(self._use_command is not None):
            self._use_command(item)

        # Remove the item from the inventory
        self.drop_item(item)

# - Main
# Used for testing code associated with this module so this code should only run when it is main
if(__name__ == "__main__"):

    # Tkinter setup
    root = tk.Tk()
    root.geometry("300x100+100+100")

    # Setup an Inventory
    invent = Inventory(print) # Associated use command is print the item
    invent.add_items([Item("Bees"),
                      Weapon("The Bee Sword", 10, 1000),
                      Armour("The Bee Chestplate", 100),
                      Potion("Potion of Bees", 20),
                      Key("The Beehive Key")])

    # Initialise a GUI representation of the GUI
    invent.gui(root)
    invent.gui_refresh()

    root.mainloop()
