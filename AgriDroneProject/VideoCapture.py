import cv2
import tellopy
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
drone = tellopy.Tello()
drone.connect()

# Create a VideoCapture object to receive video from the drone
# cap = cv2.VideoCapture('udp://@0.0.0.0:11111')  # Tello video stream
cap = cv2.VideoCapture('http://localhost:8080/video_feed')  # Tello Simulator video stream
#cap = cv2.VideoCapture('path/to/local/video.mp4')

# Create a Tkinter window
root = tk.Tk()
root.title("Tello Video Stream")

# Create a label for displaying the video feed
video_label = ttk.Label(root)
video_label.pack()

# Function to update video until connection is established
def update_video():
    ret, frame = cap.read()
    if ret:
        # Process the frame to identify crop issues
        processed_frame = process_frame(frame)

        # Convert the processed frame to a format compatible with Tkinter
        img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        video_label.img = img
        video_label.config(image=img)

        # Schedule the update function to run periodically
        root.after(10, update_video)
    else:
        # If the connection is lost, stop updating the video
        print("Connection lost. Stopping video update.")
        cap.release()

# Start the video update loop
update_video()

# Run the Tkinter main loop
root.mainloop()

# When the Tkinter main loop exits, release resources and quit the drone connection
cap.release()
drone.quit()
