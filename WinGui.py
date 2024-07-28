import tkinter as tk
from tkinter import messagebox

def submit():
    username = username_entry.get()
    password = password_entry.get()
    steam_guard_code = steam_guard_code_entry.get()
    
    # Here you can add the logic to handle the entered data
    # For now, we'll just show a message box with the entered information
    messagebox.showinfo("Submitted Information", f"Username: {username}\nPassword: {password}\nSteam Guard Code: {steam_guard_code}")

# Create the main application window
root = tk.Tk()
root.title("Installer")

# Create and place the username label and entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the password label and entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place the Steam Guard code label and entry
steam_guard_code_label = tk.Label(root, text="Steam Guard Code:")
steam_guard_code_label.grid(row=2, column=0, padx=10, pady=10)
steam_guard_code_entry = tk.Entry(root)
steam_guard_code_entry.grid(row=2, column=1, padx=10, pady=10)

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=3, columnspan=2, pady=20)

# Run the Tkinter main loop
root.mainloop()