import threading
import tkinter as tk
from tkinter import ttk
import cv2
import djitellopy
import serial
from DroneBlocksTelloSimulator import tello
from PIL import Image, ImageTk
from datetime import datetime, time

# Global variables
is_recording = False
video_writer = None

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

# Create the main application window
root = tk.Tk()
root.title("Image and Video Capture")

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Create a label for displaying the video feed
video_label = ttk.Label(root)
video_label.pack()

# Create buttons for image capture and video recording
capture_button = ttk.Button(root, text="Capture Image", command=capture_image)
capture_button.pack()

record_button = ttk.Button(root, text="Start Recording", command=toggle_record)
record_button.pack()

# Create a label for status messages
status_label = ttk.Label(root, text="")
status_label.pack()

# Function to update the video feed
def update_video():
    ret, frame = cap.read()
    if ret:
        if is_recording:
            video_writer.write(frame)

        # Display the video feed in the label
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        video_label.img = img
        video_label.config(image=img)

        # Schedule the update function to run periodically
        root.after(10, update_video)

# Start the video update loop
update_video()



# Function to process each frame
def process_frame(frame):
    # Convert the frame to grayscale for simpler processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply image processing techniques to identify crop issues
    # You can use any image processing or computer vision techniques here

    # Example: Detect edges using Canny edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Example: Find contours in the image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Example: Draw bounding boxes around detected issues
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangle

    return frame

# Initialize Tello
drone = djitellopy.Tello()
drone.connect()
drone.wait_for_connection()

# Create a VideoCapture object to receive video from the drone
cap = cv2.VideoCapture('udp://@0.0.0.0:11111')  # Tello video stream
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame to identify crop issues
    processed_frame = process_frame(frame)

    # Display the processed frame
    cv2.imshow('Crop Issues Detection', processed_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Initialize temperature sensor
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with your sensor details

# Define temperature thresholds for decision-making
TEMP_THRESHOLD_HOT = 30.0  # Adjust as needed
TEMP_THRESHOLD_COLD = 10.0  # Adjust as needed

# Function to read temperature from the sensor
def read_temperature():
    while True:
        temperature_data = ser.readline().decode('utf-8').strip()
        temperature = float(temperature_data)
        print(f"Temperature: {temperature}°C")
        time.sleep(5)  # Adjust the interval as needed

# Start a separate thread to read temperature data
temperature_thread = threading.Thread(target=read_temperature)
temperature_thread.daemon = True
temperature_thread.start()

# Function to control the drone based on temperature
def control_drone():
    while True:
        temperature = float(ser.readline().decode('utf-8').strip())

        if temperature > TEMP_THRESHOLD_HOT:
            print("It's too hot. Initiating irrigation or other actions.")
            # Add code to trigger irrigation or other actions here

        elif temperature < TEMP_THRESHOLD_COLD:
            print("It's too cold. Consider heating or delaying planting.")
            # Add code for heating or planting delay actions here

        time.sleep(600)  # Adjust the interval as needed

# Start a separate thread to control the drone based on temperature
drone_control_thread = threading.Thread(target=control_drone)
drone_control_thread.daemon = True
drone_control_thread.start()

# Main loop for drone control (takeoff, hover, and land)
try:
    tello.takeoff()
    time.sleep(5)  # Adjust as needed
    tello.move_up(50)  # Adjust as needed

    # Add more drone movements as needed

    tello.land()
except KeyboardInterrupt:
    print("Keyboard Interrupt. Landing the drone.")
    tello.land()

# Release resources

# Run the Tkinter main loop


# Release resources when the Tkinter main loop exits
cap.release()
if video_writer:
    video_writer.release()
# Release resources

# Run the Tkinter main loop
root.mainloop()
cv2.destroyAllWindows()
drone.quit()