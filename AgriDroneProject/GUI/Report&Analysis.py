from djitellopy import Tello
import time
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

# Initialize the Tello drone
drone = Tello()
drone.connect()
drone.takeoff()
drone.set_speed(90)
drone.flip_forward()


# Wait for the Tello to be ready
time.sleep(2)

# List to store drone data
altitude_data = []
time_data = []

# Flight loop to collect data
for _ in range(5):  # Collect data for 5 seconds (adjust as needed)
    altitude = drone.get_height()  # Get altitude data from the drone
    current_time = time.time()  # Get current time
    altitude_data.append(altitude)
    time_data.append(current_time)
    time.sleep(1)  # Wait for 1 second before the next iteration

# Visualize data using Matplotlib
plt.figure(figsize=(8, 6))
plt.plot(time_data, altitude_data, marker='o', linestyle='-', color='b')
plt.xlabel('Time (seconds)')
plt.ylabel('Altitude (cm)')
plt.title('Tello Drone Altitude Data')
plt.grid(True)
plt.savefig('altitude_plot.png')  # Save the plot as an image file
plt.show()

# Generate a PDF report with the visualization
pdf_filename = 'drone_report.pdf'
c = canvas.Canvas(pdf_filename)
c.setFont("Helvetica", 12)
c.drawString(50, 750, "Tello Drone Altitude Data Visualization")
c.drawImage('altitude_plot.png', 50, 500, width=400, height=300)
c.save()

# Print a message indicating the PDF generation is complete
print(f"PDF report generated: {pdf_filename}")

# Disconnect from the drone
drone.land()
drone.disconnect()
