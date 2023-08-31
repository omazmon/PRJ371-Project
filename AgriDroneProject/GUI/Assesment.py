import tkinter as tk
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from djitellopy import Tello

# Initialize the Tello drone
drone = Tello()
drone.connect()
drone.streamon()

# Load the trained machine learning model and label encoder
clf = SVC(kernel='linear', C=1)
clf.load("your_model_path")  # Load your trained model
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load("your_label_encoder_path.npy", allow_pickle=True)  # Load your label encoder

# Function to preprocess and predict crop condition from a frame
def predict_crop_condition(frame):
    frame = cv2.resize(frame, (64, 64)).flatten() / 255.0
    prediction = clf.predict([frame])
    predicted_class = label_encoder.inverse_transform(prediction)[0]
    return predicted_class

# Create a Tkinter window
root = tk.Tk()
root.title("AgriDrone Report")

# Function to calculate NDVI
def calculate_ndvi(image):
    # Convert the input image to float32
    image = image.astype(float)

    # Extract the red and near-infrared (NIR) channels
    red_channel = image[:, :, 2]
    nir_channel = image[:, :, 3]

    # Calculate NDVI
    ndvi = (nir_channel - red_channel) / (nir_channel + red_channel)

    return ndvi

# Function to identify pests or diseases
def identify_pests_or_diseases(image):

    green_channel = image[:, :, 1]  # Assuming green is the 2nd channel in the image
    threshold = 100  # Adjust this threshold as needed
    pests_detected = np.where(green_channel < threshold, 1, 0)

    return pests_detected

def capture_and_analyze():
    frame = drone.get_frame_read().frame  # Capture a frame from the Tello camera

    # Crop analysis
    crop_condition = predict_crop_condition(frame)

    # Calculate NDVI
    ndvi_result = calculate_ndvi(frame)

    # Identify pests or diseases
    pests_or_diseases_result = identify_pests_or_diseases(frame)

    # Display results
    cv2.imshow("Original Image", frame)
    cv2.imshow("NDVI", ndvi_result)
    cv2.imshow("Pests or Diseases", pests_or_diseases_result * 255)  # Convert to 8-bit for display

    # Update the analysis label
    analysis_label.config(text=f"Analysis: Crop Condition - {crop_condition}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Create a label for the analysis
analysis_label = tk.Label(root, text="Analysis:", font=("Times New Roman", 16))
analysis_label.pack()

# Create a button to trigger the analysis
analyze_button = tk.Button(root, text="Analyze Crop", command=capture_and_analyze)
analyze_button.pack()

# Run the Tkinter main loop
root.mainloop()
