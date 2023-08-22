import cv2
import numpy as np

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
    # Add your pest or disease detection logic here
    # This can involve image processing techniques, machine learning, or deep learning models

    # For demonstration, let's assume we identify pests if the green pixel value is below a threshold
    green_channel = image[:, :, 1]  # Assuming green is the 2nd channel in the image
    threshold = 100  # Adjust this threshold as needed
    pests_detected = np.where(green_channel < threshold, 1, 0)

    return pests_detected

# Load an example crop image (replace with your image file)
image_path = '  .jpg'
crop_image = cv2.imread(image_path)

# Calculate NDVI
ndvi_result = calculate_ndvi(crop_image)

# Identify pests or diseases
pests_or_diseases_result = identify_pests_or_diseases(crop_image)

# Display results
cv2.imshow("Original Image", crop_image)
cv2.imshow("NDVI", ndvi_result)
cv2.imshow("Pests or Diseases", pests_or_diseases_result * 255)  # Convert to 8-bit for display

cv2.waitKey(0)
cv2.destroyAllWindows()
