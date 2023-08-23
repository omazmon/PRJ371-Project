import subprocess
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

# Create the main application window
root = tk.Tk()
root.title("Login Form")
# Set the window size to fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# Set the background image
background_image = Image.open("background-image.jpg")  # Replace with your background image file
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Create a label for instructions
login_instructions = tk.Label(
    root,
    text="Please login using your AgriDrone credentials",
    font=("Times New Roman", 16, "bold"),
    bg="white",  # Set the background color of the label
)
login_instructions.pack(pady=20)  # Add some padding

# Function to open the application.py
def open_application():
    # Close the login form (root window)
    root.destroy()
    # Open the application.py using subprocess
    subprocess.Popen(["python", "Application.py"])  # Replace "python" with your Python executable if needed

# Define valid credentials for the technician and farmer
valid_credentials = {
    "technician": {"username": "admin", "password": "1234"},
    "farmer": {"username": "farmer", "password": "password123"}
}
# Track incorrect login attempts
incorrect_attempts = 0

# Function to validate credentials
def validate_credentials(username, password):
    user_role = None
    for role, credentials in valid_credentials.items():
        if username == credentials["username"] and password == credentials["password"]:
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
        if user_role == "technician":
            # Open the technician's form
            open_application()
        elif user_role == "farmer":
            # Open the farmer's form
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
