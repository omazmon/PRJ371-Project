import subprocess
import threading
from future.moves.tkinter import messagebox
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
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


# Function to handle keyboard input and control the drone
def control_drone():
    drone.takeoff()  # Takeoff when the application starts


def on_key_release(event):
    drone.send_rc_control(0, 0, 0, 0)  # Stop the drone when a key is released


def on_key_press(event):
    key = event.char
    if key == 'w':
        drone.send_rc_control(0, 0, 30, 0)  # Move up when 'w' is pressed
    elif key == 's':
        drone.send_rc_control(0, 0, -30, 0)  # Move down when 's' is pressed
    elif key == 'a':
        drone.send_rc_control(0, -30, 0, 0)  # Move left when 'a' is pressed
    elif key == 'd':
        drone.send_rc_control(0, 30, 0, 0)  # Move right when 'd' is pressed
    elif key == 'q':
        drone.send_rc_control(0, 0, 0, -30)  # Rotate counterclockwise when 'q' is pressed
    elif key == 'e':
        drone.send_rc_control(0, 0, 0, 30)  # Rotate clockwise when 'e' is pressed
    elif key == 'l':
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


# # Load YOLO model and class labels
# net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
#
# with open('coco.names', 'r') as f:
#     classes = f.read().strip().split('\n')

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

        # crop_condition = predict_crop_condition(frame)
        # ndvi_result = calculate_ndvi(frame)
        pests_or_diseases_result = identify_pests_or_diseases(frame)
        # object_detected_frame = identify_objects(frame)

        cv2.imshow("Original Image", frame)
        cv2.imshow("NDVI", receive_ndvi_map())
        cv2.imshow("Pests or Diseases", pests_or_diseases_result * 255)
        # cv2.imshow("Object Detection", object_detected_frame)
        #
        # analysis_label.config(text=f"Analysis: Crop Condition - {crop_condition}")

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as E:
        print(f"Error in capture_and_analyze: {E}")
        messagebox.showerror("Error", f"Error in capture_and_analyze: {E}")


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


# try:
#     crop_condition_clf = joblib.load("your_crop_condition_model_path.pkl")
# except Exception as e:
#     print(f"Error loading model: {e}")
#     # Handle the error, show a message box, or exit the program.
#     exit()
#
#
# # Function to capture and analyze

#
#
# try:
#     features = np.load('features.npy')
#     labels = np.load('labels.npy')
#     ndvi_map = cv2.imread('path_to_ndvi_map_image.jpg')
#     crop_condition_clf = SVC(kernel='linear', C=1)
#     crop_condition_clf.load("your_crop_condition_model_path")
#     crop_condition_label_encoder = LabelEncoder()
#     crop_condition_label_encoder.classes_ = np.load("your_crop_condition_label_encoder_path.npy", allow_pickle=True)
# except Exception as e:
#     print(f"Error loading data: {e}")
#     # Handle the error, show a message box, or exit the program.
#     exit()
#
#
# # Function to identify and label objects
# def identify_objects(frame):
#     detected_objects, confidences = detect_objects(frame)
#
#     for K, (x1, y1, x2, y2, class_id) in enumerate(detected_objects):
#         label = classes[class_id]
#         confidence = confidences[K]
#         text = f"{label}: {confidence:.2f}"
#
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#
#     return frame
#
#
#
#
# # Function to preprocess and predict crop condition from a frame
# def predict_crop_condition(frame):
#     frame = cv2.resize(frame, (64, 64)).flatten() / 255.0
#     prediction = crop_condition_clf.predict([frame])
#     predicted_class = crop_condition_label_encoder.inverse_transform(prediction)[0]
#     return predicted_class
#
#
# # Define color ranges for different nitrogen levels and soil types
# nitrogen_colors = {
#     (0, 0, 255): 250,  # Blue (high rate)
#     (0, 255, 255): 200,  # Yellow (medium rate)
#     (0, 255, 0): 150,  # Green (medium rate)
#     (0, 165, 255): 100,  # Orange (low rate)
#     (128, 0, 128): None  # Purple (no data)
# }
#
# soil_colors = {
#     (255, 0, 0): 'coarser texture, darker colored soil',
#     (0, 255, 255): 'coarser texture, lighter colored soil',
#     (0, 255, 0): 'nominal',
#     (0, 140, 255): 'finer texture, darker colored soil',
#     (128, 0, 128): 'finer texture, lighter colored soil'
# }
#
#
# # Function to identify nitrogen level from color
# def get_nitrogen_level(color):
#     for key in nitrogen_colors.keys():
#         if np.array_equal(color, np.array(key)):
#             return nitrogen_colors[key]
#     return None
#
#
# # Function to identify soil type from color
# def get_soil_type(color):
#     for key in soil_colors.keys():
#         if np.array_equal(color, np.array(key)):
#             return soil_colors[key]
#     return None
#
#
# # Process each pixel in the NDVI map to extract nitrogen levels and soil types
# for i in range(ndvi_map.shape[0]):
#     for j in range(ndvi_map.shape[1]):
#         pixel_color = ndvi_map[i, j]
#         nitrogen_level = get_nitrogen_level(pixel_color)
#         soil_type = get_soil_type(pixel_color)
#         if nitrogen_level is not None:
#             print(f'Nitrogen Level at pixel ({i}, {j}): {nitrogen_level}')
#         if soil_type is not None:
#             print(f'Soil Type at pixel ({i}, {j}): {soil_type}')
#
#
# # Function to calculate NDVI
# def calculate_ndvi(image):
#     # Extract the red and near-infrared (NIR) channels as float32
#     red_channel = image[:, :, 2].astype(np.float32)
#     nir_channel = image[:, :, 3].astype(np.float32)
#
#     # Calculate NDVI using vectorized operations
#     ndvi = (nir_channel - red_channel) / (nir_channel + red_channel)
#
#     return ndvi
#
#
# # Function to identify pests or diseases
# def identify_pests_or_diseases(image):
#     green_channel = image[:, :, 1]  # Assuming green is the 2nd channel in the image
#     threshold = 100  # Adjust this threshold as needed
#     pests_detected = np.where(green_channel < threshold, 1, 0)
#     return pests_detected
#
#
# # Function to perform object detection
# def detect_objects(frame):
#     # Prepare the input image for YOLO
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)
#
#     # Get the output layer names
#     output_layer_names = net.getUnconnectedOutLayersNames()
#
#     # Run YOLO forward pass to get detections
#     detections = net.forward(output_layer_names)
#
#     # Initialize lists to store detected objects and their confidences
#     detected_objects = []
#     confidences = []
#
#     # Loop over the detections
#     for detection in detections:
#         for obj in detection:
#             scores = obj[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#
#             # Filter out weak detections by setting a confidence threshold
#             if confidence > 0.5:
#                 center_x = int(obj[0] * frame.shape[1])
#                 center_y = int(obj[1] * frame.shape[0])
#                 width = int(obj[2] * frame.shape[1])
#                 height = int(obj[3] * frame.shape[0])
#
#                 # Calculate bounding box coordinates
#                 x = int(center_x - width / 2)
#                 y = int(center_y - height / 2)
#
#                 detected_objects.append((x, y, x + width, y + height))
#                 confidences.append(float(confidence))
#
#     return detected_objects, confidences


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

business_name_label = tk.Label(root, text="Agridrone", font=("Times New Roman", 24, "bold"), bg="#FFFFFF")
business_name_label.pack(pady=20)

slogan_label = tk.Label(root, text="Optimal Farming Solutions", font=("Times New Roman", 14, "italic underline"), bg="#FFFFFF")
slogan_label.pack(pady=10)
# Run the Tkinter main loop
root.mainloop()
control_drone()
