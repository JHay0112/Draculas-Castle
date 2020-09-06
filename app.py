'''

    app.py

    Author: Jordan Hay
    Date: 2020-09-06

    Dracula's Castle application/game

'''

# - Imports

# -- Libraries
# (Modules others have made)
import tkinter as tk # GUI
from tkinter import ttk # Refined GUI elements

# -- Components
# (Modules I have made)
import items # Items/Inventories
import map # Maps/Rooms

# - Classes

# - Functions

# - Main

root = tk.Tk() # Tkinter root object

# Main check
if __name__ == "__main__":

    # Tkinter setup
    root.geometry("1000x700+100+100")
    root.title("Dracula's Castle")

    # Tkinter mainloop
    root.mainloop()