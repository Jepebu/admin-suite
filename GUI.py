
def main(root):
    import tkinter as tk
    from tkinter import messagebox, simpledialog
    import subprocess
    import re
    import platform
    import pickle
    import sys
    import os
    import signal
    global tkinter_button_objects
    global dark_mode
    button_data_list = []
    dark_mode = False
    STATE_FILE = "program_state.pkl"
    
    def save_state():
        state = {
            "dark_mode": dark_mode,
            "buttons": [],
        }
        for button_obj in button_data_list:
            button_info = {
                "text": button_obj.name,
                "command": button_obj.command,
            }
            state["buttons"].append(button_info)
        with open(STATE_FILE, "wb") as file:
            pickle.dump(state, file)
        sys.exit()
        
    def load_state():
        try:
            with open(STATE_FILE, "rb") as file:
                state = pickle.load(file)
                global dark_mode
                dark_mode = state.get("dark_mode", False)
                global tkinter_button_objects
                tkinter_button_objects_data = state.get("buttons", [])
                
                # Clear existing buttons
                for button in tkinter_button_objects:
                    button.grid_forget()
                tkinter_button_objects.clear()

                for button_data in tkinter_button_objects_data:
                    button = tk.Button(root, text=button_data["text"])
                    button_command = button_data["command"]
                    button.bind("<Button-3>", lambda event, btn=button: confirm_delete_button(event, btn))
                    if dark_mode == True:
                        button.config(bg="black", fg="grey94")
                    else:
                        button.config(bg="grey94", fg="black")
                    button_data = button_object(button_data["text"],button_data["command"])
                    button.config(command=lambda cmd=button_command: run_command(cmd))
                    tkinter_button_objects.append(button)
                    row = (len(tkinter_button_objects) - 1) // 2 + 2
                    col = (len(tkinter_button_objects) - 1) % 2

                    button.grid(row=row, column=col, sticky="nsew")

                    root.grid_rowconfigure(row, weight=1)
                    root.grid_columnconfigure(col, weight=1)

        except FileNotFoundError:
            pass


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
        
        settings_window = tk.Toplevel(root)
        settings_window.title("Settings")

        def toggle_dark_mode():
            global dark_mode
            # Update the dark mode style for all buttons
            
            if dark_mode == False:
                root.config(bg="black")
            else:
                root.config(bg="grey94")
            
            for button in tkinter_button_objects:
                if dark_mode == False:
                    button.config(bg="black", fg="grey94")
                else:
                    button.config(bg="grey94", fg="black")
            dark_mode = not dark_mode

        # Create the dark mode checkbox
        dark_mode_checkbox = tk.Checkbutton(settings_window, text="Dark Mode", command=toggle_dark_mode)
        dark_mode_checkbox.pack(pady=10)
        
        
        

    def run_command(button):
        command = str(button)  # Convert command to string
        
        command = find_and_replace_variables(command)

        if platform.system() == "Windows":
            process = subprocess.Popen(['start', 'cmd', '/k', command], shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        elif platform.system() == "Linux":
            process = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        elif platform.system() == "Darwin":  # macOS
            process = subprocess.Popen(['osascript', '-e', 'tell app "Terminal" to do script "{}"'.format(command)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            
        # Write an empty command to the terminal process to keep it open
        process.stdin.write(b"\n")
        process.stdin.flush()
        
        
        
    def find_and_replace_variables(command):
        if "$" in command:
            user_input = simpledialog.askstring("Variable Input", f"Enter value for variable:")
            modified_command = re.sub('\$[A-Za-z0-9]+', user_input, command)
            return modified_command
        else:
            return command
            
            
            
    class button_object():
        def __init__(self,text,command):
            self.name = text
            self.command = command
            button_data_list.append(self)
            
            
            
            
            
    def add_button():
        if len(tkinter_button_objects) < 16:
            # Create the button configuration dialog
            dialog = ButtonConfigDialog(root, title="Button Configuration")
            
            if dialog.result:
                button = tk.Button(root, text=dialog.button_name)
                button_command = dialog.button_command
                button.bind("<Button-3>", lambda event, btn=button: confirm_delete_button(event, btn))
                
                # Set button style based on dark mode state
                if dark_mode == True:
                    button.config(bg="black", fg="grey94")
                else:
                    button.config(bg="grey94", fg="black")
                button_data = button_object(dialog.button_name,dialog.button_command)
                button["command"] = dialog.button_command
                button.config(command=lambda cmd=button_command: run_command(cmd))
                tkinter_button_objects.append(button)
                row = (len(tkinter_button_objects) - 1) // 2 + 2
                col = (len(tkinter_button_objects) - 1) % 2
                
                button.grid(row=row, column=col, sticky="nsew")
                
                root.grid_rowconfigure(row, weight=1)
                root.grid_columnconfigure(col, weight=1)
        else:
            messagebox.showinfo("Maximum Buttons Reached", "You have reached the maximum limit of buttons.")

    def confirm_delete_button(event, button):
        result = messagebox.askquestion("Confirmation", "Are you sure you want to delete this button?")
        if result == "yes":
            button.grid_forget()
            tkinter_button_objects.remove(button)
            reconfigure_grid()

    def reconfigure_grid():
        for i, button in enumerate(tkinter_button_objects):
            row = i // 2 + 2
            col = i % 2
            button.grid(row=row, column=col, sticky="nsew")
            root.grid_rowconfigure(row, weight=1)
            root.grid_columnconfigure(col, weight=1)

    #root = tk.Tk()
    root.title("Admin Suite")
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
    tkinter_button_objects = []
    load_state()
    root.protocol("WM_DELETE_WINDOW", lambda: save_state())  # Save state on window close
    root.mainloop()
