# xvfb-run python3 object-detection.py

import cv2
import numpy as np
from base_camera import BaseCamera
import os



video_source = 0
colorUpper = np.array([44, 255, 255]) 
colorLower = np.array([24, 100, 100])

# if os.environ.get('OPENCV_CAMERA_SOURCE'):
# video_source = int(os.environ['OPENCV_CAMERA_SOURCE'])  
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Could not start camera')

print(cap.isOpened)

while (cap.isOpened()) :
    ret , frame = cap.read()
    
    # cv2.rectangle(frame, (100,100), (200, 200), [255, 0, 0], 2)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(gray, colorLower, colorUpper)
    
    mask = cv2.erode(mask, None, iterations=2) 
    
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    # print(f'length of cnts is {cnts}')
    
    center = None
    
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((box_x, box_y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        print(f'coordinates of object are {M}')
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        X = int(box_x)
        Y = int(box_y)

        print('Target color object detected')
        print('X:%d'%X)
        print('Y:%d'%Y)
        print(f'center is {center}')
        print('-------')

        cv2.putText(frame,'Target Detected',(40,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
        
        cv2.rectangle(frame,(int(box_x-radius),int(box_y+radius)),
        (int(box_x+radius),int(box_y-radius)),(255,255,255),1)
        
        cv2.imshow('frame',frame)
    else:
        cv2.putText(frame,'Detecting target',(40,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1,cv2.LINE_AA)
        print('No target color object detected')
        cv2.imshow('frame',frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release ()
cv2.destroyAllWindows ()
