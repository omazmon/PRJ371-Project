import subprocess
import tkinter as tk
from tkinter import messagebox
import bcrypt
# Create the main application window
root = tk.Tk()
root.title("Login Form")

# Set the window size to fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# Create a label for instructions
login_instructions = tk.Label(
    root,
    text="Login",
    font=("Times New Roman", 24, "bold"),
    bg="white",  # Set the background color of the label
)
login_instructions.pack(pady=20)  # Add some padding

# Function to open the Application.py
def open_application():
    root.destroy()
    subprocess.Popen(["python", "Application.py"])

# Define valid credentials for the technician and farmer
valid_credentials = {
    "technician": {"username": "admin", "password": bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt())},
    "farmer": {"username": "farmer", "password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())}
}

# Track incorrect login attempts
incorrect_attempts = 0
# Function to validate credentials
def validate_credentials(username, password):
    user_role = None
    for role, credentials in valid_credentials.items():
        if username == credentials["username"] and bcrypt.checkpw(password.encode('utf-8'), credentials["password"]):
            user_role = role
            break
    return user_role

# Function to handle login button click
def login():
    global incorrect_attempts
    username = entry_username.get()
    password = entry_password.get()

    user_role = validate_credentials(username, password)

    if user_role:
        messagebox.showinfo("Success", "Login successful!")
        root.withdraw()  # Hide the login window
        open_application()
    else:
        incorrect_attempts += 1
        if incorrect_attempts >= 3:
            messagebox.showerror("Error", "Too many incorrect login attempts. The application will now close.")
            root.destroy()  # Close the application
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

# Create and place labels and entry widgets for username and password
label_username = tk.Label(root, text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")  # Mask the password with asterisks
entry_password.pack()

# Create a button to perform login
login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

# Start the Tkinter main loop
root.mainloop()
