import atexit
import os
import threading
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
import numpy as np
import pyodbc
from PIL import Image, ImageTk
from djitellopy import Tello
from future.moves.tkinter import messagebox
from keras.models import load_model
from matplotlib import contour

# Load the background image
# background_image = Image.open("background-image.jpg")
# background_photo = ImageTk.PhotoImage(background_image)
# background_label = tk.Label(root, image=background_photo)
# background_label.place(relwidth=1, relheight=1)
# Load the pre-trained pest detection model
pest_detection_model = load_model('imagemodels/PestClassifier.h5')
captured_images_directory = "captured_images"
os.makedirs(captured_images_directory, exist_ok=True)

conn_str = "DRIVER={SQL Server};SERVER=Mthokozisi-2\SQLEXPRESS;DATABASE=AgriDrone;Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
# Initialize the Tello drone
drone = Tello()
drone.connect()
drone.streamon()

total_days = 0
total_growth = 0

# Initialize the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# # Load YOLO
# net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
#
# Function to identify pests using the loaded model
def identify_pests(frame):
    # Resize the frame to match the input size of the model
    resized_frame = cv2.resize(frame, (224, 224))

    # Preprocess the frame for the model prediction
    preprocessed_frame = np.expand_dims(resized_frame, axis=0)
    preprocessed_frame = preprocessed_frame / 255.0  # Normalize pixel values

    # Perform prediction using the pest detection model
    predictions = pest_detection_model.predict(preprocessed_frame)

    # Assuming the model has binary output (1 for pest, 0 for non-pest)
    pest_detected = predictions[0][0] > 0.5

    return pest_detected


def create_report(crop_health):
    try:
        with open('crop_health_report.txt', 'a') as file:
            file.write(f'Crop Health: {crop_health}\n')

        # Update the Tkinter label with the crop health information
        crop_health_label.config(text=f"Crop Health: {crop_health}")
    except Exception as e:
        print(f"Error in create_report: {e}")
        # Handle the error, e.g., show an error message in Tkinter messagebox
        tk.messagebox.showerror("Error", f"Error in create_report: {e}")


# # Function for object detection
# def identify_objects_yolo(frame):
#     height, width, channels = frame.shape
#
#     # Detecting objects
#     blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#     net.setInput(blob)
#     outs = net.forward(output_layers)
#
#     # Information to show on the screen
#     class_ids = []
#     confidences = []
#     boxes = []
#
#     # Extract information from outs
#     for out in outs:
#         for detection in out:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#
#             if confidence > 0.5:
#                 # Object detected
#                 center_x = int(detection[0] * width)
#                 center_y = int(detection[1] * height)
#                 w = int(detection[2] * width)
#                 h = int(detection[3] * height)
#
#                 # Rectangle coordinates
#                 x = int(center_x - w / 2)
#                 y = int(center_y - h / 2)
#
#                 boxes.append([x, y, w, h])
#                 confidences.append(float(confidence))
#                 class_ids.append(class_id)
#
#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#
#     # Draw rectangles and labels on the objects detected
#     for i in range(len(boxes)):
#         if i in indexes:
#             x, y, w, h = boxes[i]
#             label = str(class_ids[i])
#             confidence = confidences[i]
#             color = (0, 255, 0)  # Green color for pests and rodents
#
#             # Draw rectangle and label
#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#             cv2.putText(frame, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
#
#     return frame
# Function to control the drone
def drone_control_thread():
    while True:
        drone.send_rc_control(0, 0, 0, 0)


# Function to update video until connection is established
def update_video_thread():
    while True:
        update_video()


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

    print(drone.get_battery())

    if key == '8':
        drone.send_rc_control(0, 0, 50, 0)  # Move up when
    elif key == '2':
        drone.send_rc_control(0, 0, -50, 2)  # Move down when
    elif key == '+':
        drone.flip_forward()
    elif key == '-':
        drone.flip_back()
    elif key == '4':
        drone.send_rc_control(-75, 0, 0, 0)
    elif key == '6':
        drone.send_rc_control(75, 0, 0, 0)
    elif key == '7':
        drone.send_rc_control(0, 0, 0, -50)  # Rotate counterclockwise when 'q' is pressed
    elif key == '9':
        drone.send_rc_control(0, 0, 0, 50)  # Rotate clockwise when 'w' is pressed
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

BG_COLOR = "#C0C0C0"  # Light gray background
LABEL_COLOR = "#333333"  # Dark gray label text
BUTTON_COLOR = "#4CAF50"  # Green button color
TEXT_COLOR = "#000000"  # Black text color
FONT_STYLE = ("Times New Roman", 14, "bold italic")  # Font style

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
copyright_label = tk.Label(root, text="Copy Right Reserved @ Agri~Drone 2023",
                           font=("Times New Roman", 14, "bold italic"))
copyright_label.pack()
takeoff_button = tk.Button(root, text="Take Off", command=take_off)
takeoff_button.pack(pady=20)
buttons_frame = tk.Frame(root)  # Create a frame to hold the buttons
buttons_frame.pack(side=tk.TOP, fill=tk.X)
battery_label = tk.Label(root, text=f"Battery level: {drone.get_battery()}%", font=FONT_STYLE, bg=BG_COLOR, fg=LABEL_COLOR)
battery_label.pack()
# Create a label for the analysis
analysis_label = tk.Label(root, text="Analysis:")
analysis_label.pack(side=tk.RIGHT)  # Span the label across all columns with padding
crop_health_label = tk.Label(root, text="", font=("Helvetica", 12))
crop_health_label.pack()
# Create a label for displaying the video feed
video_label = tk.Label(root)
video_label.pack()


# Function to update video until connection is established
def update_video():
    frame = drone.get_frame_read().frame  # Get frame from the drone's camera
    # Perform pest detection
    pest_detected = identify_pests(frame)
    # Process the frame
    processed_frame = process_frame(frame)
    if pest_detected:
        # Draw a red rectangle around the pest
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # You can also add additional text or labels to the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Pest Detected', (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        tk.messagebox.showinfo("Pest Detection", "No pests detected in the current frame.")

    # Convert the processed frame to a format compatible with Tkinter
    img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)

    # Update the label with the new frame
    video_label.img = img
    video_label.config(image=img)
    root.after(60, update_video)


def identify_pests_or_diseases(image):
    green_channel = image[:, :, 1]  # Assuming green is the 2nd channel in the image
    threshold = 100  # Adjust this threshold as needed
    pests_detected = np.where(green_channel < threshold, 1, 0)
    return pests_detected


def start_ndvi_stream():
    # Function to update video with NDVI frames
    def update_ndvi_video():
        frame = drone.get_frame_read().frame
        processed_frame = process_frame(frame)
        # processed_frame = identify_objects_yolo(processed_frame)

        # Calculate and visualize NDVI
        ndvi_image = calculate_and_visualize_ndvi(processed_frame)

        # Update the label with the new NDVI image
        video_label.img = ndvi_image
        video_label.config(image=ndvi_image)
        root.after(60, update_ndvi_video)

    # Start updating the video with NDVI frames
    update_ndvi_video()


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
    red_band = frame[:, :, 1]
    nir_band = frame[:, :, 2]

    # Calculate NDVI
    ndvi_map = (nir_band - red_band) / (nir_band + red_band)
    ndvi_map = np.nan_to_num(ndvi_map)
    # Apply a colormap for visualization (Jet colormap in this case)
    ndvi_visualized = cv2.applyColorMap(np.uint8(255 * ndvi_map), cv2.COLORMAP_JET)

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
        ndvi_value = calculate_and_visualize_ndvi(frame)
        crop_health = analyze_crop_health(ndvi_value)
        pests_or_diseases_result = identify_pests_or_diseases(frame)

        # Create a PDF report with crop health and pest detection results
        pdf_file_path = os.path.join(captured_images_directory, "report.pdf")
        with open(pdf_file_path, 'w') as file:
            file.write(f'Crop Health Report\n')
            file.write(f'NDVI Value: {ndvi_value}\n')
            file.write(f'Crop Health: {crop_health}\n')
            file.write(f'Pests or Diseases: {pests_or_diseases_result}\n')

        # Save the original frame, NDVI image, and pests or diseases detection result
        original_image_path = os.path.join(captured_images_directory, "original_frame.jpg")
        ndvi_image_path = os.path.join(captured_images_directory, "ndvi_map.jpg")
        pests_or_diseases_path = os.path.join(captured_images_directory, "pests_or_diseases_result.jpg")

        cv2.imwrite(original_image_path, frame)
        cv2.imwrite(ndvi_image_path, ndvi_value)
        cv2.imwrite(pests_or_diseases_path, pests_or_diseases_result * 255)

        # Insert image paths into the 'images' table (assuming you have a table named 'images' in the database)
        cursor.execute("INSERT INTO images (image_type, image_path) VALUES (?, ?)", ("original", original_image_path))
        cursor.execute("INSERT INTO images (image_type, image_path) VALUES (?, ?)", ("ndvi", ndvi_image_path))
        cursor.execute("INSERT INTO images (image_type, image_path) VALUES (?, ?)",
                       ("pests_or_diseases", pests_or_diseases_path))
        conn.commit()

        # Display the PDF report content to the user (optional)
        with open(pdf_file_path, 'r') as file:
            report_content = file.read()
            print(report_content)  # Print the report content to the console (you can display it in Tkinter labels)

        # Display images (optional)
        cv2.imshow("Original Image", frame)
        cv2.imshow("NDVI", ndvi_value)
        cv2.imshow("Pests or Diseases", pests_or_diseases_result * 255)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as E:
        print(f"Error in capture_and_analyze: {E}")
        messagebox.showerror("Error", f"Error in capture_and_analyze: {E}")


atexit.register(conn.close)

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
        # Automatic return to base
        drone.land()
        time.sleep(2)


# Check battery level every
def check_battery_periodically():
    while True:
        check_battery()
        time.sleep(2)


# Function to analyze crop growth
def analyze_crop_growth(previous_image_path, current_image_path):
    # Load previous and current images
    previous_image = cv2.imread(previous_image_path)
    current_image = cv2.imread(current_image_path)

    diff_image = cv2.absdiff(previous_image, current_image)

    # Count non-zero pixels (changed pixels) to calculate growth area
    changed_pixel_count = np.count_nonzero(diff_image)

    # Calculate growth percentage based on changed pixel count
    total_pixels = 2 * 1  # Assuming a fixed area for demonstration
    growth_percentage = (changed_pixel_count / total_pixels) * 100

    return growth_percentage


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


# Function to handle button click event
def on_button_click():
    previous_image_path = filedialog.askopenfilename(title="Select Previous Image")
    current_image_path = filedialog.askopenfilename(title="Select Current Image")

    # Call the analyze_crop_growth function
    growth_percentage = analyze_crop_growth(previous_image_path, current_image_path)

    # Display the output
    output_label.config(text=f"Crop Growth Percentage: {growth_percentage:.2f}%")


# Create a button to trigger the video stream
video_button = tk.Button(root, text="View stream", command=update_video, font=FONT_STYLE, bg=BG_COLOR, fg=LABEL_COLOR)  # Object Detection
video_button.pack(side=tk.LEFT, padx=5)

# Create a button to trigger the NDVI stream
ndvi_button = tk.Button(root, text="View NDVI", command=start_ndvi_stream, font=FONT_STYLE, bg=BG_COLOR, fg=LABEL_COLOR)  # Crophealth analysis(NDVI)
ndvi_button.pack(side=tk.LEFT, padx=5)

pest_button = tk.Button(root, text="Pest Detection", command=capture_and_analyze, font=FONT_STYLE, bg=BG_COLOR, fg=LABEL_COLOR)  # Pest detection
pest_button.pack(side=tk.LEFT, padx=5)

analyze_button = tk.Button(root, text="Analyze Crops", command=process_crops, font=FONT_STYLE, bg=BG_COLOR, fg=LABEL_COLOR)
analyze_button.pack(side=tk.LEFT, padx=5)

# Create a button to trigger the analysis
growth_button = tk.Button(root, text="Crop Growth", command=on_button_click)
growth_button.pack(side=tk.LEFT, padx=5)  # Place the button at row 0, column 2 with padding

# Create a button for the report
report_button = tk.Button(root, text="Generate Report", command=create_report)  # User feedback
report_button.pack(side=tk.LEFT, padx=5)  # Place the button at row 0, column 3 with padding

# Create a button for logout
logout_button = tk.Button(root, text="LogOut", command=close_application)
logout_button.pack(side=tk.BOTTOM, padx=5)

output_label = tk.Label(root, text="")
output_label.pack()
# Create threads for controlling the drone and updating the video
video_thread = threading.Thread(target=update_video_thread)
drone_thread = threading.Thread(target=drone_control_thread)
battery_thread = threading.Thread(target=check_battery_periodically)
atexit.register(close_application)
# Start the tkinter main loop (window will open here)
root.mainloop()

# Start both threads after tkinter window is closed
video_thread.start()
drone_thread.start()
battery_thread.start()
drone.streamoff()
