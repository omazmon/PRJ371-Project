import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from DroneBlocksTelloSimulator import drone

# Create a list of provinces in South Africa
provinces = ["Please select province", "Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo", "Mpumalanga", "North West", "Northern Cape", "Western Cape"]

# Create a list of top 5 farming crops in South Africa
top_crops = ["Maize", "Sugarcane", "Wheat", "Sunflower", "Citrus"]

# Create a Tkinter window
root = tk.Tk()
root.title("AgriDrone")

# Set the window size to fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# Set the background image
background_image = Image.open("background-image.jpg")  # Replace with your background image file
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Function to open the DroneData application
def open_dronedata():
    selected_province = location_combobox.get()
    farm_name = farm_name_entry.get()  # Get the farm name from the text box
    selected_crop = crop_combobox.get()  # Get the selected crop type
    if selected_province != "Please select province" and farm_name and selected_crop:
        # You can use selected_province, farm_name, and selected_crop here for further processing
        subprocess.Popen(["python", "DroneData.py"])
        root.destroy()
    else:
        messagebox.showerror("Error", "Please select a province, enter a farm name, and select a crop type.")

# Create a welcome label
welcome_label = tk.Label(root, text="Welcome to AgriDrone", font=("Times New Roman", 24, "bold"), fg="black")
welcome_label.pack()

# Create a farm name label and text box
farm_name_label = ttk.Label(root, text="Farm Name:")
farm_name_entry = ttk.Entry(root)
farm_name_label.pack()
farm_name_entry.pack()

# Create a location dropdown (combobox)
location_label = ttk.Label(root, text="Location")
location_combobox = ttk.Combobox(root, values=provinces, state="readonly")
location_combobox.set("Please select province")
location_label.pack()
location_combobox.pack()

# Create a crop type dropdown (combobox)
crop_label = ttk.Label(root, text="Crop Type")
crop_combobox = ttk.Combobox(root, values=top_crops, state="readonly")
crop_combobox.set("Select Crop Type")
crop_label.pack()
crop_combobox.pack()

# Create a button for Crop Assessment (formerly DroneData)
crop_assessment_button = ttk.Button(root, text="Drone start", command=open_dronedata)
crop_assessment_button.pack()

# Start the GUI main loop
root.mainloop()
