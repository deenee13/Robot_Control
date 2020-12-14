import time
import threading
import cv2
import zmq
import base64
import picamera
from picamera.array import PiRGBArray
import argparse
import imutils
from collections import deque
import psutil
import os
import servo
import PID
import LED
import datetime
from rpi_ws281x import *
import move
import numpy as np
import ultra
import sys

pid = PID.PID()
pid.SetKp(0.5)
pid.SetKd(0)
pid.SetKi(0)
Y_lock = 0
X_lock = 0
tor    = 17
FindColorMode = 0
WatchDogMode  = 0
UltraData = 3
LED  = LED.LED()

# Initialising the motor
print("Initialising the motor")
move.setup()



def test():
    ap = argparse.ArgumentParser()
    ap.add_argument("-b", "--buffer", type=int, default=64,
                    help="max buffer size")
    args = vars(ap.parse_args())
    pts = deque(maxlen=args["buffer"])

    font = cv2.FONT_HERSHEY_SIMPLEX
    FindColorMode = 1
    tor = 20
    X_lock = 0

    # Reading the values from the camera
    camera = picamera.PiCamera()
    
    # Resizing the resolution
    camera.resolution = (640, 480)
    
    # Setting the frame rate to 20
    camera.framerate = 20
    rawCapture = PiRGBArray(camera, size=(640, 480))
    
    # What color object to detect HSV upper and lower value of it
    colorUpper = (44, 255, 255)
    colorLower = (24, 100, 100)
    
    # for loop to continuous read the value from camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame_image = frame.array
        cv2.line(frame_image,(300,240),(340,240),(128,255,128),1)
        cv2.line(frame_image,(320,220),(320,260),(128,255,128),1)
        timestamp = datetime.datetime.now()
        cv2.imshow('frame', frame_image)
        if FindColorMode:

            ####>>>OpenCV Start<<<####
            
            # Converting image to HSV color model
            hsv = cv2.cvtColor(frame_image, cv2.COLOR_BGR2HSV)
            
            # detecting the color which is in the object
            mask = cv2.inRange(hsv, colorLower, colorUpper)
            
            # performing te erosion operation
            mask = cv2.erode(mask, None, iterations=2)
            
            # perfroming the dilation operation
            mask = cv2.dilate(mask, None, iterations=2)
            
            # Getting the coordinates of the object from the enironment
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            if len(cnts) > 0:
                cv2.putText(frame_image,'Target Detected',(40,60), font, 0.5,(0,0,255),1,cv2.LINE_AA)
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                X = int(x)
                Y = int(y)

                print(f'value of Integer X:{X} and Y:{Y} along with the center: {center}')

                cv2.rectangle(frame_image,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),(0,0,255),1)
                cv2.imshow('frame', frame_image)

                """
                if Y < (240-tor):
                    error = (240-Y)/5
                    outv = int(round((pid.GenOut(error)),0))
                    print('Servomotor will rotate up\n')#servo.camera_ang('lookup',outv)
                    Y_lock = 0
                elif Y > (240+tor):
                    error = (240-Y)/5
                    outv = int(round((pid.GenOut(error)),0))
                    print('Servomotor will rotate down\n')#servo.camera_ang('lookdown',outv)
                    Y_lock = 0
                else:
                    Y_lock = 1
                    print('Y_lock = 1 in it\n')
                """
                
                # Sccording to the coordnates deciding  which side to move and by how much delay
                if X < (320-tor):
                    print(f'motor will move left in X with value {X}')####move.move(70, 'no', 'left', 0.6)
                    move.move(60, 'no', 'left', 0.6)
                    time.sleep(0.5)
                    move.motorStop()
                elif X > (320+tor):
                    print(f'motor will move right in X with value {X}')####move.move(70, 'no', 'right', 0.6)
                    move.move(60, 'no', 'right', 0.6)
                    time.sleep(0.3)
                    move.motorStop()
               
                elif X >= 300 and X < 310:
                    print(f'motor will move slight left with X value {X}')####move.motorStop()
                    move.move(40, 'no', 'left', 0.6)
                    time.sleep(0.04)
                    move.motorStop()

                elif X >= 310 and X < 320:
                    print(f'motor will move left with X value {X}')
                    move.move(40, 'no', 'left', 0.6)
                    time.sleep(0.02)
                    move.motorStop()
                    
                elif X > 320 and X <= 340:
                    print(f'motor will move slight right with X value {X}')
                    move.move(40, 'no', 'right', 0.6)
                    time.sleep(0.02)
                    move.motorStop()

                elif X > 330 and X <= 340:
                    print(f'motore will move slight right with X value {X}')
                    move.move(40, 'no', 'right', 0.6)
                    time.sleep(0.04)
                    move.motorStop()

                else:
                    print('lock in X')
                    X_lock = 1
                                    
                                    
                                    
                if X >= 317 and X <= 320:           #if X == 320:
                    
                    X_lock = 0
                    ultradata = ultra.checkdist()
                    time.sleep(0.5) 
                    if ultradata >= 0.1:
                        LED.colorWipe(255,16,0)
                        # move motor forward
                        print(f'motor will move forward and dist {ultradata}')
                        move.move(30, 'forward', 'no', 0.6)
                        time.sleep(0.30)
                        move.motorStop()

                    elif ultradata > 0.06 and ultradata < 0.1:
                        LED.colorWipe(255,16,0)
                        # move motor forward
                        print(f'motor will move forward and dist {ultradata}')
                        move.move(30, 'forward', 'no', '0.6')
                        time.sleep(0.10)
                        move.motorStop()
                            
                    elif ultradata < 0.06:
                        LED.colorWipe(0,16,255)
                        # move motor backward
                        print(f'motor will move backward and dist {ultradata}')
                        move.move(30, 'backward', 'no', 0.6)
                        time.sleep(0.10)
                        move.motorStop()
                        
                    else:
                        #stop the motor
                        print(f'motor will stop with dist {ultradata}')
                        move.motorStop()
                        sys.exit()
                        break
                
            else:
                cv2.putText(frame_image,'Target detecting',(40,60), font, 0.5,(255,0,0),1,cv2.LINE_AA)
                print('Servo motor is not rotating')
                cv2.imshow('frame', frame_image)
                '''
                while 1:

                    ultradata = ultra.checkdist()
                    time.sleep(0.5)
                    if ultradata > 0.06:
                        LED.colorWipe(255,16,0)
                        print(f'motor will move forward and dist {ultradata}')
                        move.move(30, 'forward', 'no', 0.6)
                        time.sleep(0.3)
                        move.motorStop()

                    elif ultradata < 0.06:
                        LED.colorWipe(0, 16, 255)
                        print(f'motor will move backward and dist {ultradata}')
                        move.move(30, 'backward', 'no', 0.6)
                        time.sleep(0.3)
                        move.motorStop()

                    else:
                        print(f'motor will stop with dist {ultradata}')
                        move.motorStop()
                        sys.exit()
                '''
                ####cv2.imshow('frame', frame_image)

            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame_image, pts[i - 1], pts[i], (0, 0, 255), thickness)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break


        rawCapture.truncate(0)


if __name__ == '__main__':

    test()
