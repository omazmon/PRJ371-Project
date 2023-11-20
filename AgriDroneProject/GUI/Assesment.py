import os
import threading
import time
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pyodbc
from PIL import Image, ImageTk
from djitellopy import Tello
from future.moves.tkinter import messagebox
import datetime

captured_images_directory = "captured_images"
os.makedirs(captured_images_directory, exist_ok=True)
# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
conn_str = "DRIVER={SQL Server};SERVER=Mthokozisi-2\SQLEXPRESS;DATABASE=AgriDrone;Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
# Initialize the Tello drone
drone = Tello()
drone.connect()
drone.streamon()

ndvi_mode = False
# Initialize the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def create_report():
    try:
        timestamp = datetime.datetime.now()
        crop_health = analysis_label.cget("text")  # Get the crop health information from the label

        # Generate the content of the report
        report_content = f'Report generated on {timestamp}:\nCrop Health: {crop_health}\n'

        # Define the report file path
        report_file_path = "crop_health_report.txt"

        # Write the report content to a text file
        with open(report_file_path, "w") as report_file:
            report_file.write(report_content)

        # Show a success message to the user
        tk.messagebox.showinfo("Report Generated", "The report has been successfully generated.")

        # Open the report file in the default text editor (you can replace this with a specific application)
        os.system(f"notepad.exe {report_file_path}")

    except Exception as e:
        print(f"Error in create_report: {e}")
        tk.messagebox.showerror("Error", f"Error in create_report: {e}")


# Function to control the drone
def drone_control_thread():
    while True:
        drone.send_rc_control(0, 0, 0, 0)


# Function to update video until connection is established
# def update_video_thread():
#     while True:
#         if ndvi_mode:
#             start_ndvi_stream()
#         else:
#             update_video()
#         time.sleep(0.1)


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

        # Save the output image with transparency
        cv2.imwrite('output_transparent_ndvi_map.png', output_image)

        # Display the output image
        cv2.imshow('Transparent NDVI Map', output_image)

        # Break the loop and close windows if 'f' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('f'):
            break


def on_key_release():
    drone.send_rc_control(0, 0, 0, 0)  # Stop the drone when a key is released


def take_off():
    drone.takeoff()
    drone.set_speed(50)


def on_key_press(event):
    key = event.char

main
    if key == '8':

    print(drone.get_battery())

    if key == 'w':
      main
        drone.send_rc_control(0, 0, 50, 0)  # Move up when
    elif key == 's':
        drone.send_rc_control(0, 0, -50, 2)  # Move down when
    elif key == '+':
        drone.flip_forward()
    elif key == '-':
        drone.flip_back()
    elif key == '4':
        drone.send_rc_control(-75, 0, 0, 0)
    elif key == '6':
main
        drone.send_rc_control(75, 0, 0, 0)
    elif key == '7':
        drone.send_rc_control(0, 0, 0, -250)  #
    elif key == '9':
        drone.send_rc_control(0, 0, 0, 250)  # Rotate clockwise when 'w' is pressed
    elif key == '0':
        take_off()
    elif key == '5':
        drone.send_rc_control(0, 0, 0, 0)  # Stop the drone when a key is released
    elif key == '.':
        drone.land()
    elif key == '1':
        drone.send_rc_control(0, 75, 0, 0)
    elif key == '3':
        drone.send_rc_control(0, -75, 0, 0)
        
        drone.send_rc_control(0, 75, 0, 0)
    elif key == '8':
        drone.send_rc_control(0, 50, 0, 0)
    elif key == '2':
        drone.send_rc_control(0, -50, 0, 0)
    elif key == 'e':
        drone.send_rc_control(0, 0, 0, -50)  # Rotate counterclockwise when 'q' is pressed
    elif key == 'q':
        drone.send_rc_control(0, 0, 0, 50)  # Rotate clockwise when 'w' is pressed
    elif key == 't':
        take_off()
    elif key == '5':
        drone.send_rc_control(0, 0, 0, 0)  # Stop the drone when a key is released
    elif key == 'l':
        drone.land()  # Land when spacebar is pressed
main


# Define color codes and their corresponding transparency values
color_transparency = {
    (0, 0, 255): 250,  # Blue (high rate)
    (0, 255, 255): 200,  # Yellow (medium rate)
    (0, 255, 0): 150,  # Green (medium rate)
    (0, 165, 255): 100,  # Orange (low rate)
    (128, 0, 128): 0  # Purple (no data)
}

# Create a Tkinter window
root = tk.Tk()
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)
root.title("Agri~Drone")
LABEL_COLOR = "#333333"
BUTTON_COLOR = "#4CAF50"  # Green color
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"
FONT_STYLE = ("Arial ", 16)

root.config(bg=BG_COLOR)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

buttons_frame = tk.Frame(root)  # Create a frame to hold the buttons
buttons_frame.pack(side=tk.TOP, fill=tk.X)

battery_label = tk.Label(root, text=f"Battery level: {drone.get_battery()}%", font=FONT_STYLE, bg=BG_COLOR,
                         fg=LABEL_COLOR)
battery_label.pack()
# Create a label for the analysis
analysis_label = tk.Label(root, text="Analysis.", font=FONT_STYLE, bg=BG_COLOR,
                          fg=LABEL_COLOR)
analysis_label.pack()  # Span the label across all columns with padding

# Create a label for displaying the video feed
video_label = tk.Label(root)
video_label.pack()


# Function to update video until connection is established
def update_video():
    global ndvi_mode
    ndvi_mode = False
    frame = drone.get_frame_read().frame

    # Process the frame using your custom processing function
    processed_frame = process_frame(frame)
    out = cv2.VideoWriter('output_video.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

    processed_frame = cv2.resize(processed_frame, (1250, 550))

    img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)
    out.write(processed_frame)
    # Update the label with the new frame
    video_label.img = img
    video_label.config(image=img)

    # Schedule the function to run again after a delay (e.g., 30 milliseconds)
    root.after(30, update_video)
    out.release()


def capture_and_save_image():
    try:
        # Capture a frame from the drone's camera
        frame = drone.get_frame_read().frame

        # Generate a unique filename for the captured image (you may use timestamps or other methods)
        image_filename = f"captured_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"

        # Save the captured image to the specified directory
        image_path = os.path.join(captured_images_directory, image_filename)
        cv2.imwrite(image_path, frame)

        # Insert image information into the database
        cursor.execute("INSERT INTO images (image_type, image_path) VALUES (?, ?)", ("captured_image", image_path))
        conn.commit()

        print(f"Image captured and saved as {image_filename}")
    except Exception as e:
        print(f"Error capturing and saving image: {e}")
        tk.messagebox.showerror("Error", f"Error capturing and saving image: {e}")


def identify_pests_or_diseases(image):
    green_channel = image[:, :, 1]  # Assuming green is the 2nd channel in the image
    threshold = 100  # Adjust this threshold as needed
    pests_detected = np.where(green_channel < threshold, 1, 0)
    return pests_detected


# Function to update video until connection is established
def update_video_thread():
    if not ndvi_mode:
        update_video()
    root.after(100, update_video_thread)


# Function to start NDVI stream
def start_ndvi_stream():
    global ndvi_mode
    ndvi_mode = True

    # Function to update video with NDVI frames
    def update_ndvi_video():
        if ndvi_mode:
            frame = drone.get_frame_read().frame
            processed_frame = process_frame(frame)

            # Calculate and visualize NDVI
            ndvi_image = calculate_and_visualize_ndvi(processed_frame)

            # Update the label with the new NDVI image
            video_label.img = ndvi_image
            video_label.config(image=ndvi_image)
            root.after(60, update_ndvi_video)

    ndvi_thread = threading.Thread(target=update_ndvi_video)
    ndvi_thread.start()

    # Start updating the video with NDVI frames
    update_ndvi_video()

#
# def start_ndvi_stream():
#     global ndvi_mode
#     ndvi_mode = True
#
#     # Function to update video with NDVI frames
#     def update_ndvi_video():
#         if ndvi_mode:
#             frame = drone.get_frame_read().frame
#             processed_frame = process_frame(frame)
#
#             # Calculate and visualize NDVI
#             ndvi_image = calculate_and_visualize_ndvi(processed_frame)
#
#             # Update the label with the new NDVI image
#             video_label.img = ndvi_image
#             video_label.config(image=ndvi_image)
#             root.after(60, update_ndvi_video)
#
#     ndvi_thread = threading.Thread(target=update_ndvi_video)
#     ndvi_thread.start()
#     # Start updating the video with NDVI frames
#     update_ndvi_video()
#

def get_soil_type(color):
    soil_colors = {
        (255, 0, 0): 'coarser texture, darker colored soil',
        (0, 255, 255): 'coarser texture, lighter colored soil',
        (0, 255, 0): 'nominal',
        (0, 140, 255): 'finer texture, darker colored soil',
        (128, 0, 128): 'finer texture, lighter colored soil'
    }

    # Function to calculate the Euclidean distance between two colors
    def color_distance(c1, c2):
        return np.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)

    # Find the closest color in the dictionary
    closest_color = min(soil_colors, key=lambda x: color_distance(color, x))

    # Return the corresponding soil type
    return soil_colors.get(closest_color, None)


def calculate_and_visualize_ndvi(frame):
    # Extract red and near-infrared bands from the frame
    red_band = frame[:, :, 0].astype(float)
    nir_band = frame[:, :, 1].astype(float)

    # Calculate NDVI
    ndvi_map = (nir_band - red_band) / (nir_band + red_band)
    ndvi_map = np.nan_to_num(ndvi_map)  # Handle division by zero

    # Scale NDVI values to the range [0, 255] for visualization
    ndvi_visualized = cv2.normalize(ndvi_map, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # Apply a colormap for visualization (Jet colormap in this case)
    ndvi_visualized = cv2.applyColorMap(ndvi_visualized, cv2.COLORMAP_JET)

    # Convert to RGB format for PIL and Tkinter compatibility
    ndvi_visualized_rgb = cv2.cvtColor(ndvi_visualized, cv2.COLOR_BGR2RGB)

    # Convert to ImageTk format
    img = Image.fromarray(ndvi_visualized_rgb)
    img_tk = ImageTk.PhotoImage(image=img)

    return img_tk


def visualize_ndvi(ndvi_map):
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


def capture_and_analyze():
    try:
        frame = drone.get_frame_read().frame

        # Optimize image processing here
        processed_frame, detected_crops = process_crops(frame)

        # Analyze the detected crops
        crop_health = analyze_crop_health(detected_crops)

        # Create a PDF report with crop health and pest detection results
        create_report(crop_health)

        # Update the Tkinter label with the crop health information
        analysis_label.config(text=f"Crop Health: {crop_health}")

    except Exception as e:
        print(f"Error in capture_and_analyze: {e}")
        messagebox.showerror("Error", f"Error in capture_and_analyze: {e}")


top_crops = ["Maize", "Sugarcane", "Wheat", "Sunflower", "Citrus"]
crop_colors = {
    "Maize": (0, 255, 0),  # Green color for Maize
    "Sugarcane": (0, 0, 255),  # Red color for Sugarcane
    "Wheat": (255, 0, 0),  # Blue color for Wheat
    "Sunflower": (0, 255, 255),  # Yellow color for Sunflower
    "Citrus": (255, 255, 0)  # Cyan color for Citrus
}


def process_crops(frame):
    # Convert the frame to HSV for color-based segmentation
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for each crop color (you need to adjust these values)
    lower_boundaries = {
        "Maize": np.array([35, 100, 100]),
        "Sugarcane": np.array([0, 100, 100]),
        "Wheat": np.array([20, 100, 100]),
        "Sunflower": np.array([15, 100, 100]),
        "Citrus": np.array([25, 100, 100])
    }
    upper_boundaries = {
        "Maize": np.array([90, 255, 255]),
        "Sugarcane": np.array([10, 255, 255]),
        "Wheat": np.array([40, 255, 255]),
        "Sunflower": np.array([30, 255, 255]),
        "Citrus": np.array([35, 255, 255])
    }

    # Initialize an empty list to store detected crops
    detected_crops = []

    # Detect crops and draw rectangles around them
    for crop, (lower, upper) in zip(top_crops, zip(lower_boundaries.values(), upper_boundaries.values())):
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), crop_colors[crop], 2)
            detected_crops.append(crop)

    return frame, detected_crops


def process_frame(frame):
    # Convert the frame to grayscale  detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Example: Detect edges using Canny edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Example: Find contours in the image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Example: Draw bounding boxes around detected issues
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangle
    # Detect faces using Haar cascade
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.circle(frame, (x + w // 2, y + h // 2), min(w, h) // 2, (0, 255, 0),
                   2)  # Draw a green circle around the face

    # Convert the frame to HSV for color-based object detection (e.g., cars)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for the blue color (for cars)
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])

    # Threshold the HSV image to get only blue colors
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours in the blue mask
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw blue rectangles around objects detected as cars
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw a blue rectangle around the object

    return frame


def close_application():
    drone.land()
    messagebox.showinfo("LogOut successful!", "AgriDrone disconnected and Goodbye")
    root.destroy()


def check_battery():
    battery_level = drone.get_battery()
    # Low battery warning
    if battery_level < 20:
        battery_label.config(text="Low Battery Warning! Returning to Base.")
        drone.land()
        time.sleep(2)


# Check battery level every
def check_battery_periodically():
    while True:
        check_battery()
        time.sleep(2)


# Function to calculate crop area
def calculate_crop_area(image):
    # Implement logic to calculate crop area based on image processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_area = 0
    for contour in contours:
        total_area += cv2.contourArea(contour)

    return total_area


def process_analyze_report():
    try:
        # Analyze the crop health and detect pests (replace this with your actual analysis logic)
        frame = drone.get_frame_read().frame
        crop_health, pests_detected = process_frame(frame)

        # Generate the content of the report
        timestamp = datetime.datetime.now()
        report_content = f'Report generated on {timestamp}:\nCrop Health: {crop_health}\nPests Detected: {pests_detected}\n'

        # Insert the report into the database
        cursor.execute("INSERT INTO AnalysisReports (report_text) VALUES (?)", (report_content,))
        conn.commit()

        # Define the report file path
        report_file_path = "crop_health_report.txt"

        # Write the report content to a text file
        with open(report_file_path, "w") as report_file:
            report_file.write(report_content)

        # Show a success message to the user
        tk.messagebox.showinfo("Report Generated",
                               "The report has been successfully generated and saved to the database.")

        # Open the report file in the default text editor (you can replace this with a specific application)
        os.system(f"notepad.exe {report_file_path}")

    except Exception as e:
        print(f"Error in process_analyze_report: {e}")
        tk.messagebox.showerror("Error", f"Error in process_analyze_report: {e}")


# Create a button to trigger the video stream
video_button = tk.Button(root, text="View stream 4 object detection", command=update_video, font=FONT_STYLE,
                         bg=BG_COLOR,
                         fg=LABEL_COLOR)  # Object Detection
video_button.pack(side=tk.LEFT, padx=5)

# Create a button to trigger the NDVI normalized difference vegetation index stream
ndvi_button = tk.Button(root, text="View NDVI", command=start_ndvi_stream, font=FONT_STYLE, bg=BG_COLOR,
                        fg=LABEL_COLOR)  # Crophealth analysis(NDVI)
ndvi_button.pack(side=tk.LEFT, padx=5)

# Create a button to trigger the analysis
analyze_button = tk.Button(root, text="Analyze Crops and Pests", command=capture_and_analyze, font=FONT_STYLE,
                           bg=BG_COLOR,
                           fg=LABEL_COLOR)
analyze_button.pack(side=tk.LEFT, padx=5)

# Create a button for the report
report_button = tk.Button(root, text="Generate Report", command=create_report,
                          font=FONT_STYLE,
                          bg=BG_COLOR,
                          fg=LABEL_COLOR)  # User feedback
report_button.pack(side=tk.LEFT, padx=5)  # Place the button at row 0, column 3 with padding
# Create a button for capturing an image
capture_image_button = tk.Button(root, text="Capture Image", command=capture_and_save_image, font=FONT_STYLE,
                                 bg=BG_COLOR, fg=LABEL_COLOR)
capture_image_button.pack(side=tk.LEFT, padx=5)

analyze_report_button = tk.Button(root, text="Analyze and Generate Report", command=process_analyze_report,
                                  font=FONT_STYLE, bg=BG_COLOR, fg=LABEL_COLOR)
analyze_report_button.pack(side=tk.LEFT, padx=5)

# Create threads for controlling the drone and updating the video
video_thread = threading.Thread(target=update_video_thread)
drone_thread = threading.Thread(target=drone_control_thread)
battery_thread = threading.Thread(target=check_battery_periodically)

video_thread.start()
drone_thread.start()
battery_thread.start()
# Start the tkinter main loop (window will open here)
root.mainloop()
