import subprocess
import tkinter as tk
from tkinter import messagebox
import bcrypt
from PIL import Image, ImageTk

# Create the main application window
root = tk.Tk()
root.title("Login Form")

# Set a consistent color scheme
BG_COLOR = "#C0C0C0"
LABEL_COLOR = "#333333"
BUTTON_COLOR = "#4CAF50"
# Load the background image
background_image = Image.open("background-image.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set the window size to a fixed size for better appearance
root.geometry("270x250")


# Function to open the Application.py
def open_application():
    root.destroy()
    subprocess.Popen(["python", "Application.py"])


valid_credentials = {
    "technician": {"username": "admin", "password": bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt())},
    "farmer": {"username": "farmer", "password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())}
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
        root.withdraw()
        open_application()
    else:
        messagebox.showerror("Error", "Invalid credentials. Please try again.")

label_username = tk.Label(root, text="Username:", bg=BG_COLOR, fg=LABEL_COLOR)
label_username.pack(pady=10)
entry_username = tk.Entry(root)
entry_username.pack(pady=10, padx=20)

label_password = tk.Label(root, text="Password:", bg=BG_COLOR, fg=LABEL_COLOR)
label_password.pack(pady=10)
entry_password = tk.Entry(root, show="*")  # Mask the password with asterisks
entry_password.pack(pady=10, padx=20)

login_button = tk.Button(root, text="Login", command=login, bg=BUTTON_COLOR, fg="white")
login_button.pack(pady=20)


root.mainloop()
