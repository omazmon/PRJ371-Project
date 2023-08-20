from djitellopy import Tello
from time import sleep
import cv2

conn = Tello()

# Set the IP and port for the Tello Simulator
conn.connect('127.0.0.1', 11111)

conn.streamon()

while True:
    img = conn.get_frame_read().frame
    # img = cv2.resize(img,(360,240))
    cv2.imshow("image", img)
    cv2.waitKey(1)
