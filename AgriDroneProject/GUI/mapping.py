import math
import cv2
from djitellopy import tello
from Controls import KeyPressModule as kp
import numpy as np

##MAPPING SHOWS WHERE THE DRONE IS AND WHERE IT HAS GONE AS WELL AS CO_ORDINATES

####Parameteres for mapping (test values)####


fSpeed = 117 / 10  ##forward speed in cm/s
aSpeed = 360 / 10  ##rotation speed in degrees/s
interval = 0.25

dInterval = fSpeed * interval
aInterval = aSpeed * interval

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
x, y = 500, 500
a = 0
yaw = 0


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    d = 0
    global x, y, yaw, a

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed

    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = speed
        yaw += aInterval
    elif kp.getKey("d"):
        yv = -speed
        yaw -= aInterval
    # yv turns the drone clockwise and anti-clockwise

    if kp.getKey("q"): me.land()
    if kp.getKey("e"): me.takeoff()

    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    ###THIS CODE IS PIN POINT THE DRONE MOVEMENTS AND DISPLAY IT ON THE SCREEN

    cv2.circle(img, (points[0], points[1]), 5, (0, 0, 255), cv2.FILLED)


while True:
    vals = getKeyboardInput()

    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    points = (vals[4], vals[5])
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
