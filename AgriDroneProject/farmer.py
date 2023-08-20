import tkinter as tk
from tkinter import messagebox
import sqlite3

def save_farmer_data():
    # Retrieve data from the input fields
    farmer_name = entry_name.get()
    farmer_location = entry_location.get()
    farmer_contact = entry_contact.get()

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('../AgriDronDatabase.sql')  # Replace with your database file name

        # Create a cursor
        cursor = connection.cursor()

        # Define the SQL query to insert the data into the Farmers table
        query = "INSERT INTO Farmers (Name, Location, Contact) VALUES (?, ?, ?)"
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

# Create the main application window
root = tk.Tk()
root.title("Farmer Data Input Form")

# Create and place labels and entry widgets for data input
label_name = tk.Label(root, text="Farmer Name:")
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

label_location = tk.Label(root, text="Location:")
label_location.pack()
entry_location = tk.Entry(root)
entry_location.pack()

label_contact = tk.Label(root, text="Contact Number:")
label_contact.pack()
entry_contact = tk.Entry(root)
entry_contact.pack()

# Create a button to save the data
save_button = tk.Button(root, text="Save Farmer Data", command=save_farmer_data)
save_button.pack()

# Start the Tkinter main loop
root.mainloop()
