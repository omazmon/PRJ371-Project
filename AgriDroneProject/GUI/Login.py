import subprocess
import tkinter as tk
from tkinter import messagebox
import bcrypt
from PIL import Image, ImageTk

# Create the main application window
root = tk.Tk()
root.title("Agri~Drone")

# Set a consistent color scheme
BG_COLOR = "#90EE90"  # Light green
LABEL_COLOR = "#333333"
BUTTON_COLOR = "#008000"  # Darker green

# Load the background image
background_image = Image.open("C:/Users/mo/OneDrive/Desktop/Year_end_Project/OIP.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Set the window size to match the background image size
root.geometry(f"{background_image.width}x{background_image.height}")


# Function to open the Application.py
def open_application():
    subprocess.Popen(["python", "Application.py"])


valid_credentials = {
    "technician": {"username": "admin", "password": bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt())},
    "farmer": {"username": "farmer", "password": bcrypt.hashpw("@1234@".encode('utf-8'), bcrypt.gensalt())}
}

# Create a label to display the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)


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
        root.destroy()
    else:
        messagebox.showerror("Error", "Invalid credentials. Please try again.")


label_Welcome = tk.Label(root, text="Login", font=("Arial", 16, "bold"))
label_Welcome.pack(pady=10)
label_username = tk.Label(root, text="Username:", fg=LABEL_COLOR)
label_username.pack(pady=10)
entry_username = tk.Entry(root)
entry_username.pack(pady=10, padx=20)

label_password = tk.Label(root, text="Password:", fg=LABEL_COLOR)
label_password.pack(pady=10)
entry_password = tk.Entry(root, show="*")  # Mask the password with asterisks
entry_password.pack(pady=10, padx=20)

login_button = tk.Button(root, text="Login", command=login, bg=BUTTON_COLOR, fg="white")
login_button.pack(pady=20)
copyright_label = tk.Label(root, text="Copy Right Reserved @ Agri~Drone 2023", bg=BG_COLOR,
                           font=("Times New Roman", 12, "bold italic"))
copyright_label.pack()
root.mainloop()