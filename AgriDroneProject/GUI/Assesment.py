import tkinter as tk
import cv2
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from djitellopy import Tello
import numpy as np
from sklearn.svm import SVC

# Load the pre-extracted features and labels
features = np.load('features.npy')
labels = np.load('labels.npy')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Initialize and train a Support Vector Machine (SVM) classifier
clf = SVC(kernel='linear', C=1)
clf.fit(X_train, y_train)

# Predict on the test set
y_pred = clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Initialize the Tello drone
drone = Tello()
drone.connect()
drone.streamon()

# Load the trained machine learning model and label encoder for crop condition
crop_condition_clf = SVC(kernel='linear', C=1)
crop_condition_clf.load("your_crop_condition_model_path")  # Load your trained crop condition model
crop_condition_label_encoder = LabelEncoder()
crop_condition_label_encoder.classes_ = np.load("your_crop_condition_label_encoder_path.npy", allow_pickle=True)  # Load your label encoder

# Create a Tkinter window
root = tk.Tk()
root.title("AgriDrone Report")

# Function to preprocess and predict crop condition from a frame
def predict_crop_condition(frame):
    frame = cv2.resize(frame, (64, 64)).flatten() / 255.0
    prediction = crop_condition_clf.predict([frame])
    predicted_class = crop_condition_label_encoder.inverse_transform(prediction)[0]
    return predicted_class

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
