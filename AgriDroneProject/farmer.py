import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyodbc


def save_farmer_data():
    # Retrieve data from the input fields
    farmer_name = entry_name.get()
    farmer_location = combo_province.get()  # Get the selected province
    farmer_contact = entry_contact.get()

    try:
        # Connect to the SQLite database
        connection = pyodbc.connect('../AgriDrone.sql')  # Replace with your database file name

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

root = tk.Tk()
root.title("Farmer Data Input Form")

# Create and place labels and entry widgets for data input
label_name = tk.Label(root, text="Farmer Name:")
label_name.pack()

entry_name = tk.Entry(root)
entry_name.pack()

label_Location = tk.Label(root, text="Location:")
label_Location.pack()

# List of South African provinces
provinces = ["Please choose a region", "Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo", "Mpumalanga", "North West", "Northern Cape", "Western Cape"]

# Create a Combobox for selecting a province
combo_province = ttk.Combobox(root, values=provinces)
combo_province.set("Please choose a region")  # Set the default value
combo_province.pack()

label_contact = tk.Label(root, text="Contact Number:")
label_contact.pack()

entry_contact = tk.Entry(root)
entry_contact.pack()

# Create a button to save the data
save_button = tk.Button(root, text="Save Farmer Data", command=save_farmer_data)
save_button.pack()

# Start the Tkinter main loop
root.mainloop()
