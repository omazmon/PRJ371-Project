import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Create the main application window
root = tk.Tk()
root.title("AgriDrone Login")

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
image = Image.open("background-image.jpg")  # Replace with your image file path
image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
background_image = ImageTk.PhotoImage(image)
# Create a frame for the login form
login_frame = tk.Frame(root, bg="white", bd=5)
login_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.6, anchor="center")

# Create a label for instructions
login_instructions = tk.Label(
    login_frame,
    text="Please login using your AgriDrone credentials",
    font=("Arial", 14, "bold"),
    bg="white",
)
login_instructions.pack(pady=10)

# Create and place labels and entry widgets for username and password
label_username = tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="white")
label_username.pack(pady=5)
entry_username = tk.Entry(login_frame, font=("Arial", 12))
entry_username.pack()

label_password = tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="white")
label_password.pack(pady=5)
entry_password = tk.Entry(login_frame, show="*", font=("Arial", 12))
entry_password.pack()

# Function to open the Application.py
def open_application():
    root.destroy()
    subprocess.Popen(["python", "Application.py"])

# Function to handle login button click
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Simulate user validation (replace with your validation logic)
    if username == "admin" and password == "1234":
        messagebox.showinfo("Success", "Login successful!")
        root.withdraw()  # Hide the login window
        open_application()
    else:
        messagebox.showerror("Error", "Invalid credentials. Please try again.")

# Create a login button
login_button = tk.Button(
    login_frame,
    text="Login",
    command=login,
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
)
login_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
