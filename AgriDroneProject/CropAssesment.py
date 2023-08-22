import cv2
import numpy as np

# Function to calculate NDVI
def calculate_ndvi(image):
    # Extract the red and near-infrared (NIR) channels
    red_channel = image[:, :, 2]
    nir_channel = image[:, :, 3]

    # Calculate NDVI
    ndvi = (nir_channel - red_channel) / (nir_channel + red_channel)

    return ndvi

# Function to identify pests or diseases (placeholder for more advanced methods)
def identify_pests_or_diseases(image):
    # Add your pest or disease detection logic here
    # This can involve image processing techniques, machine learning, or deep learning models

    # For demonstration, let's assume no pests or diseases
    return np.zeros_like(image[:, :, 0])

# Load your crop image (replace with the actual image path)
image_path = 'your_crop_image.jpg'
crop_image = cv2.imread(image_path)

if crop_image is None:
    print("Error: Image not found.")
else:
    # Calculate NDVI
    ndvi_result = calculate_ndvi(crop_image)

    # Identify pests or diseases
    pests_or_diseases_result = identify_pests_or_diseases(crop_image)

    # Display results
    cv2.imshow("Original Image", crop_image)
    cv2.imshow("NDVI", (ndvi_result * 255).astype(np.uint8))  # Scale NDVI to 8-bit for display
    cv2.imshow("Pests or Diseases", (pests_or_diseases_result * 255).astype(np.uint8))  # Convert to 8-bit for display

    cv2.waitKey(0)
    cv2.destroyAllWindows()
