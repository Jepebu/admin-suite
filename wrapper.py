from GUI import main
import tkinter as tk
import sys


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    main()
    root.destroy()
    sys.exit()