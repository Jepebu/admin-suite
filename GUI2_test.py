import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess

dark_mode = False  # Variable to track dark mode state

class ButtonConfigDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Button Name:").grid(row=0, sticky="e")
        tk.Label(master, text="Button Command:").grid(row=1, sticky="e")

        self.name_entry = tk.Entry(master)
        self.command_entry = tk.Entry(master)

        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.command_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def apply(self):
        self.button_name = self.name_entry.get()
        self.button_command = self.command_entry.get()
        self.result = True

def open_settings_window():
    global dark_mode  # Access the global variable
    
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    def toggle_dark_mode():
        global dark_mode  # Access the global variable
        dark_mode = not dark_mode

        # Update the dark mode style for all buttons
        for button in buttons:
            if dark_mode:
                button.config(bg="black", fg="grey94")
            else:
                button.config(bg="grey94", fg="black")

    # Create the dark mode checkbox
    dark_mode_checkbox = tk.Checkbutton(settings_window, text="Dark Mode", command=toggle_dark_mode)
    dark_mode_checkbox.pack(pady=10)

def run_command(command):
    subprocess.run(command, shell=True)

def add_button():
    if len(buttons) < 16:
        # Create the button configuration dialog
        dialog = ButtonConfigDialog(root, title="Button Configuration")
        
        if dialog.result:
            button = tk.Button(root, text=dialog.button_name,
                               command=lambda cmd=dialog.button_command: run_command(cmd))
            button.bind("<Button-3>", lambda event, btn=button: confirm_delete_button(event, btn))
            
            # Set button style based on dark mode state
            if dark_mode:
                button.config(bg="black", fg="grey94")
            else:
                button.config(bg="grey94", fg="black")
            
            buttons.append(button)
            row = (len(buttons) - 1) // 2 + 2
            col = (len(buttons) - 1) % 2
            button.grid(row=row, column=col, sticky="nsew")
            root.grid_rowconfigure(row, weight=1)
            root.grid_columnconfigure(col, weight=1)

def confirm_delete_button(event, button):
    result = messagebox.askquestion("Confirmation", "Are you sure you want to delete this button?")
    if result == "yes":
        button.grid_forget()
        buttons.remove(button)
        reconfigure_grid()

def reconfigure_grid():
    for i, button in enumerate(buttons):
        row = (i // 2) + 2
        col = i % 2
        button.grid(row=row, column=col, sticky="nsew")
        root.grid_rowconfigure(row, weight=1)
        root.grid_columnconfigure(col, weight=1)

root = tk.Tk()
root.title("Button GUI")
root.minsize(400, 300)  # Set minimum size of the window

# Create a frame for the settings and add button
settings_frame = tk.Frame(root, height=50)
settings_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Create the settings button
settings_button = tk.Button(settings_frame, text="Settings", command=open_settings_window)
settings_button.pack(side="left", padx=10, pady=10)

# Create the add button
add_button = tk.Button(settings_frame, text="+", command=add_button)
add_button.pack(side="right", padx=10, pady=10)

# Configure grid weights
root.grid_rowconfigure(0, weight=0)  # Top row

# Maintain a list to keep track of buttons
buttons = []

root.mainloop()
