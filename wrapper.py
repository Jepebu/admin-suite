from GUI import main
import tkinter as tk
import sys


if __name__ == "__main__":
    root = tk.Tk()
    main(root)
    root.withdraw()  # Hide the root window
    