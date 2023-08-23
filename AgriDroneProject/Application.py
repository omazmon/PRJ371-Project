import subprocess
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tellopy

# Create a Tkinter window
root = tk.Tk()
root.title("AgriDrone Movement")
# Set the window size to fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# Set the background image
background_image = Image.open("background-image.jpg")  # Replace with your background image file
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)
# Function to open the DroneData application
def open_dronedata():
    root.destroy()
    subprocess.Popen(["python", "DroneData.py"])
drone = tellopy.Tello()
# Function to take off
def takeoff():
    drone.takeoff()
    print("Taking off...")

# Function to land
def land():
    drone.land()
    print("Landing...")
# Create buttons for DroneData application,takeoff and land
takeoff_button = ttk.Button(root, text="Takeoff", command=takeoff)
land_button = ttk.Button(root, text="Land", command=land)
dronedata_button = ttk.Button(root, text="DroneData", command=open_dronedata)
# Layout the widgets
takeoff_button.pack()
land_button.pack()
dronedata_button.pack()

# Start the GUI main loop
root.mainloop()
