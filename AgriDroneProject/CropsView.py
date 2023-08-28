import DroneBlocksTelloSimulator
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from DroneBlocksTelloSimulator import drone
# Create a Tkinter window
root = tk.Tk()
root.title("AgriDrone Report")

# Set the window size to fullscreen
root.attributes('-fullscreen', True)

# Function to exit fullscreen mode (press Esc to exit)
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

# Bind the Escape key to exit fullscreen mode
root.bind('<Escape>', exit_fullscreen)

# Set the background image
background_image = Image.open("background-image.jpg")  # Replace with your background image file
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Create a label for the analysis
analysis_label = tk.Label(root, text="Analysis:", font=("Times New Roman", 16))
analysis_label.pack()

# Create a panel for the "Report from AgriDrone"
report_panel = tk.LabelFrame(root, text="Report from AgriDrone", font=("Times New Roman", 16))
report_panel.pack(padx=10, pady=10)

# Create a label to display the video/image (replace with your logic)
video_label = tk.Label(report_panel, text="Video/Image Placeholder", font=("Times New Roman", 12))
video_label.pack()

# Function to handle Tello sensor data
def handle_tello_data(event, sender, data):
    if event == "data":
        # Parse the log data to extract sensor information (not available in the simulator)
        pass

# Create a Tello Simulator object
drone = DroneBlocksTelloSimulator.drone()
try:
    # Connect to the Tello Simulator
    drone.connect()

    # Start receiving video stream (you can capture frames here)
    drone.start_video()

    # Function to update the video frame
    def update_video_frame():
        # Capture video frame from the Tello Simulator (replace this with your image processing logic)
        frame = drone.read_video_frame()

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
