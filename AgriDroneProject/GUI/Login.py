import subprocess
import time
import tkinter as tk
from tkinter import messagebox
import bcrypt

# Create the main application window
root = tk.Tk()
root.title("Agri~Drone")

# Set a consistent color scheme for the application
BG_COLOR = "#C0C0C0"  # Light gray background
LABEL_COLOR = "#333333"  # Dark gray label text
BUTTON_COLOR = "#4CAF50"  # Green button color
TEXT_COLOR = "#000000"  # Black text color
FONT_STYLE = ("Times New Roman", 14, "bold italic")  # Font style

# Set the window size to a fixed size for better appearance
root.geometry("400x360")
root.config(bg=BG_COLOR)  # Set the background color of the window


# Function to open the Application.py
def open_application():
    subprocess.Popen(["python", "Application.py"])


valid_credentials = {
    "technician": {"username": "admin", "password": bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt())},
    "farmer": {"username": "farmer", "password": bcrypt.hashpw("@1234@".encode('utf-8'), bcrypt.gensalt())}
}


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
    username = entry_username.get()
    password = entry_password.get()

    user_role = validate_credentials(username, password)

    if user_role:
        messagebox.showinfo("Success", f"Welcome, {username.capitalize()}!")
        open_application()
        time.sleep(3)
        root.destroy()
    else:
        messagebox.showerror("Error", "Invalid credentials. Please try again.")


# Labels and Entries for username and password
label_Welcome = tk.Label(root, text="Welcome to AgriDrone", font=FONT_STYLE, bg=BG_COLOR, fg=TEXT_COLOR)
label_Welcome.pack()
label_Login = tk.Label(root, text="Please Login!", font=FONT_STYLE, bg=BG_COLOR, fg=TEXT_COLOR)
label_Login.pack(pady=10)
label_username = tk.Label(root, text="Username:", font=FONT_STYLE, bg=BG_COLOR, fg=LABEL_COLOR)
label_username.pack(pady=10)
entry_username = tk.Entry(root, font=FONT_STYLE)
entry_username.pack(pady=10, padx=20)

label_password = tk.Label(root, text="Password:", font=FONT_STYLE, bg=BG_COLOR, fg=LABEL_COLOR)
label_password.pack(pady=10)
entry_password = tk.Entry(root, show="*", font=FONT_STYLE)  # Mask the password with asterisks
entry_password.pack(pady=10, padx=20)

# Login button with specified color and font style
login_button = tk.Button(root, text="Login", command=login, bg=BUTTON_COLOR, fg="white", font=FONT_STYLE)
login_button.pack(pady=20)

# Copyright label
copyright_label = tk.Label(root, text="Copy Right Reserved @ Agri~Drone 2023", font=FONT_STYLE, bg=BG_COLOR,
                           fg=TEXT_COLOR)
copyright_label.pack()

# Start the tkinter main loop
root.mainloop()
