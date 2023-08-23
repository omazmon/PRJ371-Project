import cv2
import tellopy
# Function to handle Tello sensor data
def handle_tello_data(event, sender, data):
    if event is tellopy.EVENT_LOG_DATA:
        # Parse the log data to extract sensor information
        log_data = data.decode('utf-8')
        sensor_data = parse_sensor_data(log_data)
        if sensor_data:
            handle_sensor_data(sensor_data)

# Function to parse Tello sensor data
def parse_sensor_data(log_data):
    sensor_data = {}
    lines = log_data.splitlines()
    for line in lines:
        if line.startswith('TempHeight'):
            parts = line.split(':')
            if len(parts) == 2:
                try:
                    temperature = float(parts[1])
                    sensor_data['temperature'] = temperature
                except ValueError:
                    pass  # Handle parsing errors here
    return sensor_data

# Function to handle sensor data (replace with your desired logic)
def handle_sensor_data(sensor_data):
    if 'temperature' in sensor_data:
        temperature = sensor_data['temperature']
        print(f"Temperature: {temperature}°C")

# Create a Tello object
drone = tellopy.Tello()

try:
    # Connect to the Tello drone
    drone.connect()

    # Listen for Tello log data events (including sensor data)
    drone.subscribe(tellopy.EVENT_LOG_DATA, handle_tello_data)

    # Start receiving video stream (you can capture frames here)
    drone.start_video()

    # Enter the main loop
    while True:
        # Capture video frame from the Tello (replace this with your image processing logic)
        frame = drone.get_frame_read().frame

        # Process the frame (e.g., display it)
        cv2.imshow("Tello Video", frame)

        # Handle key press events (e.g., exit on 'q')
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Release resources
    drone.stop_video()
    drone.quit()
    cv2.destroyAllWindows()

