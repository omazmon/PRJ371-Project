import cv2
from djitellopy import tello
import KeyPressModule as kp
import numpy as np

from time import sleep

##MAPPING SHOWS WHERE THE DRONE IS AND WHERE IT HAS GONE AS WELL AS CO_ORDINATES

####Parameteres for mapping (test values)####



fSpeed = 117/10  ##forward speed in cm/s
aSpeed = 360/10  ##rotation speed in degrees/s
interval = 0.25

dInterval = fSpeed*interval
aInterval = aSpeed*interval



kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed

    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = speed
    elif kp.getKey("d"):
        yv = -speed
    # yv turns the drone clockwise and anti-clockwise

    if kp.getKey("q"): me.land()
    if kp.getKey("e"): me.takeoff()

    return [lr, fb, ud, yv]

def drawPoints():
###THIS CODE IS PIN POINT THE DRONE MOVEMENTS AND DISPLAY IT ON THE SCREEN

    cv2.circle(img,(300, 500),5,(0,0,255), cv2.FILLED)

while True:
    vals = getKeyboardInput()

    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    drawPoints()
    cv2.imshow("Output",img)
    cv2.waitKey(1)



