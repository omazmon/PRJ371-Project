import subprocess
import time
import tkinter as tk
from PIL import Image, ImageTk
from droneblocks.DroneBlocksTello import DroneBlocksTello

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
tello = DroneBlocksTello()
# Function to open the DroneData application
def open_dronedata():
    subprocess.Popen(["python", "Crops.py"])
    root.destroy()


# Function to take off
def takeoff():
    flight_status_label.config(text="Flight Status: Flying...", fg="green")
    tello.takeoff()
    flight_status_label.config(text="Flight Status: ..Stationary", fg="black")
    time.sleep(3)

# Function to land
def land():
    flight_status_label.config(text="Flight Status: Landing...", fg="red")
    tello.land()
    flight_status_label.config(text="Flight Status: Landed", fg="black")
    time.sleep(3)

# Create a welcome label
welcome_label = tk.Label(root, text="Welcome to AgriDrone!", font=("Times New Roman", 24, "bold"), fg="black")
welcome_label.pack()

# Create a label for flight status
flight_status_label = tk.Label(root, text="Flight Status: Stationary", font=("Times New Roman", 16), fg="black")
flight_status_label.pack()

# Create a panel for basic movement controls
basic_movement_frame = tk.LabelFrame(root, text="Basic Movement", font=("Times New Roman", 16))
basic_movement_frame.pack(padx=10, pady=10)

# Create buttons for takeoff and land within the panel
takeoff_button = tk.Button(basic_movement_frame, text="Takeoff", command=takeoff, bg="green")
land_button = tk.Button(basic_movement_frame, text="Land", command=land, bg="red")

# Layout the buttons within the panel
takeoff_button.pack(padx=10, pady=5)
land_button.pack(padx=10, pady=5)

# Create a "DroneData" button outside the panel
dronedata_button = tk.Button(root, text="Report & Analysis", command=open_dronedata)
dronedata_button.pack(pady=10)

# Start the GUI main loop
root.mainloop()
