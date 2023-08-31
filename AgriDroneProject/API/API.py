import threading
from flask import Flask, request, jsonify
import cap
import logging

from AgriDroneProject.GUI.DroneGui import toggle_record, capture_image, root

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('agri_drone.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ... Import necessary libraries ...

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
    except Exception as e:
        logger.error(f"Error toggling video recording: {str(e)}")
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
