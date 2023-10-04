import subprocess
import threading
from future.moves.tkinter import messagebox
import tkinter as tk
import cv2
from tkinter import messagebox
import numpy as np
from djitellopy import Tello
from PIL import Image, ImageTk

# Initialize the Tello drone
drone = Tello()
drone.connect()
drone.streamon()

# Define the minimum allowed distance to objects in centimeters
MIN_DISTANCE = 30
# Function to handle keyboard input and control the drone
def control_drone():
    drone.takeoff()
    drone.set_speed(50)
    # Loop for controlling the drone
    while True:
        # Get distance information from the drone's sensors (assuming the function is available)
        distance = drone.get_distance_tof()
        # Check if the distance to the object is less than the minimum allowed distance
        if distance < MIN_DISTANCE:
            # If the object is too close, hover in place and do not move forward
            drone.send_rc_control(0, 0, 0, 0)
        else:
            # If the object is at a safe distance, you can send movement commands as before
            # Example: Move forward with a speed of 30
            drone.send_rc_control(0, 30, 0, 0)


def on_key_release():
    drone.send_rc_control(0, 0, 0, 0)  # Stop the drone when a key is released


def on_key_press(event):
    key = event.char
    if key == 'w':
        drone.send_rc_control(0, 0, 30, 0)  # Move up when 'w' is pressed
    elif key == 's':
        drone.send_rc_control(0, 0, -30, 0)  # Move down when 's' is pressed
    elif key == 'a':
        drone.send_rc_control(0, -30, 0, 5)  # Move left when 'a' is pressed
    elif key == 'd':
        drone.send_rc_control(0, 30, 0, 5)  # Move right when 'd' is pressed
    elif key == 'q':
        drone.send_rc_control(0, 0, 0, -30)  # Rotate counterclockwise when 'q' is pressed
    elif key == 'e':
        drone.send_rc_control(0, 0, 0, 30)  # Rotate clockwise when 'e' is pressed
    elif key == ' ':
        drone.land()  # Land when spacebar is pressed


# Function to control the drone
def drone_control_thread():
    control_drone()


# Function to update video until connection is established
def update_video_thread():
    while True:
        update_video()


# Create a Tkinter window
root = tk.Tk()
root.title("AgriDrone Assesment")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

# Define color codes and their corresponding transparency values
color_transparency = {
    (0, 0, 255): 250,  # Blue (high rate)
    (0, 255, 255): 200,  # Yellow (medium rate)
    (0, 255, 0): 150,  # Green (medium rate)
    (0, 165, 255): 100,  # Orange (low rate)
    (128, 0, 128): 0  # Purple (no data)
}


# Function to receive and process NDVI map image
def receive_ndvi_map():
    while True:
        frame = drone.get_frame_read().frame

        # Process the frame (assuming the NDVI map is in a specific region of the frame)
        ndvi_map = frame[30:30, 30:30]

        # Apply transparency based on color codes
        for i in range(ndvi_map.shape[0]):
            for j in range(ndvi_map.shape[1]):
                pixel_color = tuple(ndvi_map[i, j])
                if pixel_color in color_transparency:
                    alpha = color_transparency[pixel_color]
                    ndvi_map[i, j] = (ndvi_map[i, j][0], ndvi_map[i, j][1], ndvi_map[i, j][2], alpha)

        # Create a transparent PNG image
        output_image = np.zeros((ndvi_map.shape[0], ndvi_map.shape[1], 4), dtype=np.uint8)
        output_image[:, :, :3] = ndvi_map
        output_image[:, :, 3] = 255  # Set alpha channel to 255 for non-transparent pixels

        # Save the output image with transparency (optional)
        cv2.imwrite('output_transparent_ndvi_map.png', output_image)

        # Display the output image (optional)
        cv2.imshow('Transparent NDVI Map', output_image)

        # Break the loop and close windows if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and destroy windows
    drone.streamoff()
    cv2.destroyAllWindows()


# Function to update video until connection is established
def update_video():
    try:
        frame = drone.get_frame_read().frame  # Get frame from the drone's camera

        # Process the frame
        processed_frame = process_frame(frame)

        # Convert the processed frame to a format compatible with Tkinter
        img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        video_label.img = img
        video_label.config(image=img)
        root.after(10, update_video)
    except Exception as E:
        print(f"Error in update_video: {E}")
        messagebox.showerror("Error", f"Error in update_video: {E}")
        # Function to identify pests or diseases


def identify_pests_or_diseases(image):
    green_channel = image[:, :, 1]  # Assuming green is the 2nd channel in the image
    threshold = 100  # Adjust this threshold as needed
    pests_detected = np.where(green_channel < threshold, 1, 0)
    return pests_detected


# Function to identify soil type from color
def get_soil_type(color):
    soil_colors = {
        (255, 0, 0): 'coarser texture, darker colored soil',
        (0, 255, 255): 'coarser texture, lighter colored soil',
        (0, 255, 0): 'nominal',
        (0, 140, 255): 'finer texture, darker colored soil',
        (128, 0, 128): 'finer texture, lighter colored soil'
    }
    for key in soil_colors.keys():
        if np.array_equal(color, np.array(key)):
            return soil_colors[key]
    return None


def capture_and_analyze():
    try:
        frame = drone.get_frame_read().frame

        # Calculate NDVI
        ndvi_map = calculate_ndvi(frame)

        # Detect pests or diseases
        pests_or_diseases_result = identify_pests_or_diseases(frame)

        # Analyze crop health
        crop_health = analyze_crop_health(ndvi_map)

        # Display NDVI map
        cv2.imshow("NDVI Map", ndvi_map)

        # Display pests or diseases detection result
        cv2.imshow("Pests or Diseases", pests_or_diseases_result * 255)

        # Provide feedback to the user
        analysis_label.config(text=f"Analysis: Crop Health - {crop_health}")

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as E:
        print(f"Error in capture_and_analyze: {E}")
        messagebox.showerror("Error", f"Error in capture_and_analyze: {E}")


def calculate_ndvi(frame):
    # Extract the Red and NIR bands from the frame (assuming specific channels)
    red_band = frame[:, :, 2]
    nir_band = frame[:, :, 3]

    # Calculate NDVI
    ndvi_map = (nir_band - red_band) / (nir_band + red_band)
    ndvi_map = np.nan_to_num(ndvi_map)  # Handle potential division by zero issues

    # Apply a colormap for visualization (optional)
    ndvi_visualized = cv2.applyColorMap(np.uint8(255 * ndvi_map), cv2.COLORMAP_JET)

    return ndvi_visualized


def analyze_crop_health(ndvi_map):
    average_ndvi = np.mean(ndvi_map)

    if average_ndvi >= 0.8:
        return "Healthy"
    elif 0.5 <= average_ndvi < 0.8:
        return "Moderate Stress"
    else:
        return "Severe Stress"


# def capture_and_analyze():
#     try:
#         frame = drone.get_frame_read().frame
#
#         # crop_condition = predict_crop_condition(frame)
#         # ndvi_result = calculate_ndvi(frame)
#         pests_or_diseases_result = identify_pests_or_diseases(frame)
#         # object_detected_frame = identify_objects(frame)
#
#         cv2.imshow("Original Image", frame)
#         cv2.imshow("NDVI", receive_ndvi_map())
#         cv2.imshow("Pests or Diseases", pests_or_diseases_result * 255)
#         # cv2.imshow("Object Detection", object_detected_frame)
#         #
#         # analysis_label.config(text=f"Analysis: Crop Condition - {crop_condition}")
#
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#
#     except Exception as E:
#         print(f"Error in capture_and_analyze: {E}")
#         messagebox.showerror("Error", f"Error in capture_and_analyze: {E}")
#

# Function to process each frame
def process_frame(frame):
    # Convert the frame to grayscale for simpler processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Example: Detect edges using Canny edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Example: Find contours in the image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Example: Draw bounding boxes around detected issues
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangle

    return frame


def close_application():
    messagebox.showinfo("Goodbye", "LogOut successful!")
    root.destroy()


def open_application():
    subprocess.Popen(["python", "Report&Analysis.py"])
    root.destroy()


# Create a button to trigger the video stream
video_button = tk.Button(root, text="View stream", command=update_video)
video_button.pack()
# Create a label for the analysis
analysis_label = tk.Label(root, text="Analysis:", font=("Times New Roman", 16))
analysis_label.pack()
# Create a label for displaying the video feed
video_label = tk.Label(root)
video_label.pack()

# Create a button to trigger the analysis
analyze_button = tk.Button(root, text="Analyze Crop", command=capture_and_analyze)
analyze_button.pack()

report_button = tk.Button(root, command=open_application)
report_button.pack()

logout_button = tk.Button(root, text="LogOut", command=close_application)
logout_button.pack()
# Create threads for controlling the drone and updating the video
drone_thread = threading.Thread(target=drone_control_thread)
video_thread = threading.Thread(target=update_video_thread)

# Start both threads
drone_thread.start()
video_thread.start()

root.mainloop()
control_drone()
