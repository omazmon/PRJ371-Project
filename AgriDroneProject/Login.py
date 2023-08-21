import tkinter as tk
from tkinter import messagebox
# Define valid credentials for the technician and farmer
valid_credentials = {
    "technician": {"username": "admin", "password": "1234"},
    "farmer": {"username": "farmer", "password": "password123"}
}

def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check if the entered credentials are valid
    user_role = None
    for role, credentials in valid_credentials.items():
        if username == credentials["username"] and password == credentials["password"]:
            user_role = role
            break

    if user_role:
        show_user_form(user_role)
    else:
        messagebox.showerror("Error", "Invalid credentials. Please try again.")

def show_user_form(user_role, login_frame=None):
    login_frame.destroy()  # Destroy the login form

    # Create and display the user-specific form
    if user_role == "farmer":
        farmer_form = tk.Toplevel(root)
        farmer_form.title("Farmer Form")

        # Add farmer-specific widgets here

        # Example: Label and entry for crop name
        label_crop_name = tk.Label(farmer_form, text="Crop Name:")
        label_crop_name.pack()
        entry_crop_name = tk.Entry(farmer_form)
        entry_crop_name.pack()

    elif user_role == "technician":
        technician_form = tk.Toplevel(root)
        technician_form.title("Technician Form")

        # Add technician-specific widgets here

        # Example: Label and entry for equipment ID
        label_equipment_id = tk.Label(technician_form, text="Equipment ID:")
        label_equipment_id.pack()
        entry_equipment_id = tk.Entry(technician_form)
        entry_equipment_id.pack()

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
