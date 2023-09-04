import datetime
import subprocess
import time
import tkinter as tk
from tkinter import ttk
import cap
import cv2
from PIL import Image, ImageTk
from droneblocks.DroneBlocksTello import DroneBlocksTello
from future.moves.tkinter import messagebox

# Create a Tkinter window
root = tk.Tk()
root.title("AgriDrone")

# Set the window size to fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# Create a panel for the "Report from AgriDrone"
report_panel = tk.LabelFrame(root, text="Report from AgriDrone", font=("Times New Roman", 16))
report_panel.pack(padx=10, pady=10)

video_label = tk.Label(report_panel, text="Video/Image Placeholder", font=("Times New Roman", 12))
video_label.pack()

drone = DroneBlocksTello()


# Function to open the DroneData application
def open_dronedata():
    subprocess.Popen(["python", "Assesment.py"])
    root.destroy()


# Function to handle Tello sensor data
def handle_tello_data(event, sender, data):
    if event == "data":
        # Parse the log data to extract sensor information (not available in the simulator)
        pass


try:
    # Connect to the Tello Simulator
    drone.connect()
    # Start receiving video stream (you can capture frames here)
    drone.stream_on()


    # Function to take off
    def takeoff():
        flight_status_label.config(text="Flight Status: Flying...", fg="green")
        drone.takeoff()
        flight_status_label.config(text="Flight Status: ..Stationary", fg="black")
        time.sleep(3)


    # Function to land
    def land():
        flight_status_label.config(text="Flight Status: Landing...", fg="red")
        drone.land()
        flight_status_label.config(text="Flight Status: Landed", fg="black")
        time.sleep(3)


    # Function to start or stop video recording
    def toggle_record():
        global is_recording, video_writer
        if is_recording:
            is_recording = False
            video_writer.release()
            record_button.config(text="Start Recording")
        else:
            is_recording = True
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d%H%M%S")
            video_filename = f"video_{timestamp}.avi"
            video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 30, (640, 480))
            record_button.config(text="Stop Recording")


    # Function to capture an image
    def capture_image():
        ret, frame = cap.read()
        if ret:
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d%H%M%S")
            image_filename = f"image_{timestamp}.jpg"
            cv2.imwrite(image_filename, frame)
            status_label.config(text=f"Image saved as {image_filename}")


    # Function to update the video frame
    def update_video_frame():
        # Capture video frame from the Tello Simulator (replace this with your image processing logic)
        frame = drone.get_frame_read()

        if frame is not None:
            # Process the frame (e.g., display it)
            cv2.imshow("Tello Video", frame)

            # Update the label with the processed frame
            video_photo = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            video_label.configure(image=video_photo)
            video_label.image = video_photo

        # Call this function again after a delay (e.g., 100 milliseconds)
        root.after(100, update_video_frame)


    # Start updating the video frame
    update_video_frame()

    # Start the GUI main loop
    root.mainloop()

except Exception as e:
    print(f"Error: {str(e)}")


def close_application():
    messagebox.showinfo("Goodbye", "LogOut successful!")
    root.destroy()


status_label = ttk.Label(root, text="")
status_label.pack()

# Create a welcome label
welcome_label = tk.Label(root, text="Drone Operations", font=("Times New Roman", 24, "bold"), fg="black")
welcome_label.pack()

# Create a label for flight status
flight_status_label = tk.Label(root, text="Flight Status: Stationary", font=("Times New Roman", 16), fg="black")
flight_status_label.pack()

# Create a panel for basic movement controls
basic_movement_frame = tk.LabelFrame(root, text="Basic Movement", font=("Times New Roman", 16))
basic_movement_frame.pack(padx=10, pady=10)

steam_options_frame = tk.LabelFrame(root, text="Stream Options:", font=("Times New Roman", 16))
steam_options_frame.pack(padx=10, pady=10)
# Create buttons for takeoff and land within the panel
takeoff_button = tk.Button(basic_movement_frame, text="Takeoff", command=takeoff, bg="green")
land_button = tk.Button(basic_movement_frame, text="Land", command=land, bg="red")

# Layout the buttons within the panel
takeoff_button.pack(padx=10, pady=5)
land_button.pack(padx=10, pady=5)

record_button = ttk.Button(steam_options_frame, text="Start Recording", command=toggle_record)
capture_button = ttk.Button(steam_options_frame, text="Capture Image", command=capture_image)

capture_button.pack(padx=25, pady=5)
record_button.pack(padx=25, pady=5)

# Create a "DroneData" button outside the panel
dronedata_button = tk.Button(root, text="Report & Analysis", command=open_dronedata)
dronedata_button.pack(pady=45)

logout_button = tk.Button(root, text="LogOut", command=close_application)
logout_button.pack(pady=55)
# Start the GUI main loop
root.mainloop()
