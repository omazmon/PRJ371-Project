import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc

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
    if login_frame:
        login_frame.destroy()  # Destroy the login form

    # Create and display the user-specific form
    user_form = tk.Toplevel()
    user_form.title(f"{user_role.capitalize()} Form")

    if user_role == "farmer":
        create_farmer_form(user_form)
    elif user_role == "technician":
        create_technician_form(user_form)

def create_farmer_form(form):
    # Add farmer-specific widgets here

    # Example: Label and entry for crop name
    label_crop_name = tk.Label(form, text="Crop Name:")
    label_crop_name.pack()
    entry_crop_name = tk.Entry(form)
    entry_crop_name.pack()

    def save_farmer_data():
        # Retrieve data from the input fields
        farmer_name = entry_name.get()
        farmer_location = combo_province.get()  # Get the selected province
        farmer_contact = entry_contact.get()

        try:
            # Connect to the SQL Server database
            connection = pyodbc.connect(
                'Driver={SQL Server};Server=your_server_name;Database=your_database_name;Trusted_Connection=yes;')

            # Create a cursor
            cursor = connection.cursor()

            # Define the SQL query to insert the data into the Farmers table
            query = "INSERT INTO farm(Name, Location, Contact) VALUES (?, ?, ?)"
            cursor.execute(query, (farmer_name, farmer_location, farmer_contact))

            # Commit the transaction
            connection.commit()

            # Close the database connection
            connection.close()

            # Show a confirmation message
            messagebox.showinfo("Success", "Farmer data saved successfully!")

        except Exception as e:
            # Handle any database-related errors
            messagebox.showerror("Error", f"Error saving data: {str(e)}")

    label_name = tk.Label(form, text="Farmer Name:")
    label_name.pack()

    entry_name = tk.Entry(form)
    entry_name.pack()

    label_Location = tk.Label(form, text="Location:")
    label_Location.pack()

    # List of South African provinces
    provinces = ["Please choose a region", "Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo",
                 "Mpumalanga", "North West", "Northern Cape", "Western Cape"]

    # Create a Combobox for selecting a province
    combo_province = ttk.Combobox(form, values=provinces)
    combo_province.set("Please choose a region")  # Set the default value
    combo_province.pack()

    label_contact = tk.Label(form, text="Contact Number:")
    label_contact.pack()

    entry_contact = tk.Entry(form)
    entry_contact.pack()

    # Create a button to save the data
    save_button = tk.Button(form, text="Save Farmer Data", command=save_farmer_data)
    save_button.pack()

def create_technician_form(form):
    # Add technician-specific widgets here

    # Example: Label and entry for equipment ID
    label_equipment_id = tk.Label(form, text="Equipment ID:")
    label_equipment_id.pack()
    entry_equipment_id = tk.Entry(form)
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
