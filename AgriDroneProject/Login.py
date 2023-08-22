import tkinter as tk
from tkinter import messagebox

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
            show_user_form(user_role)
        elif user_role == "farmer":
            # Open the farmer's form
            show_user_form(user_role)
    else:
        incorrect_attempts += 1
        if incorrect_attempts >= 3:
            messagebox.showerror("Error", "Too many incorrect login attempts. The application will now close.")
            root.destroy()  # Close the application
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

# Function to create user-specific form
def show_user_form(user_role):
    # Create and display the user-specific form
    user_form = tk.Toplevel()
    user_form.title(f"{user_role.capitalize()} Form")

    if user_role == "farmer":
        create_farmer_form(user_form)
    elif user_role == "technician":
        create_technician_form(user_form)

# Function to create farmer-specific form
def create_farmer_form(form):
    # Add farmer-specific widgets here
    pass

# Function to create technician-specific form
def create_technician_form(form):
    # Add technician-specific widgets here
    pass

# Create the main application window
root = tk.Tk()
root.title("Login Form")

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
