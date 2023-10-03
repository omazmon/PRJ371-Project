import threading
from flask import Flask, request, jsonify
import logging
from keras.src.applications.densenet import layers
from requests import models
from AgriDroneProject.GUI.Assesment import X_train, y_train, X_test, y_test
from AgriDroneProject.GUI.DroneGui import toggle_record, capture_image, root


# Define the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')  # num_classes is the number of crop conditions
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model using your prepared dataset
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy * 100:.2f}%")

# Save the trained model and label encoder
model.save("crop_condition_model.h5")

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('agri_drone.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Define your configuration variables
irrigation_threshold = 0.4

# Create a Flask app
app = Flask(__name__)


# Define API routes
@app.route('/api/start_recording', methods=['POST'])
def api_start_recording():
    try:
        # Start/stop video recording
        toggle_record()
        return jsonify({"message": "Video recording toggled"}), 200
    except Exception as E:
        logger.error(f"Error toggling video recording: {str(E)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/capture_image', methods=['POST'])
def api_capture_image():
    try:
        # Capture an image
        capture_image()
        return jsonify({"message": "Image captured"}), 200
    except Exception as e:
        logger.error(f"Error capturing image: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    try:
        # Start both the Tkinter and Flask applications in separate threads
        t1 = threading.Thread(target=root.mainloop)
        t2 = threading.Thread(target=app.run, kwargs={"debug": True})

        t1.start()
        t2.start()
    except Exception as e:
        logger.error(f"Error starting threads: {str(e)}")
