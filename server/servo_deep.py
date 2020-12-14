#!/usr/bin/env python3
# File name   : servo_deep.py
# Description : Servo Control Motor
# Author      : Deepen Parmar(parmar@pdx.edu)
# Date        : 2020/12/09

import RPIservo
import time


# Algorithm to move arm down
def arm_down():
    
    print('Arm will go down\n')
    H1_sc.singleServo(12, -1, 1)
    H2_sc.singleServo(13, -1, 1)
    time.sleep(7)
    H1_sc.stopWiggle()
    H2_sc.stopWiggle()

# Algorithm to move gripper
def arm_gripper():
    print('Gripper will Grab the ball\n')
    G_sc.singleServo(15, 1, 1)
    time.sleep(3)
    G_sc.stopWiggle()

# Algorithm to move arm up
def arm_up():
    print('Arm will go up\n')
    H1_sc.singleServo(12, 1, 3)
    H2_sc.singleServo(13, 1, 3)
    time.sleep(7)
    H1_sc.stopWiggle()
    H2_sc.stopWiggle()
    
# Initialse the servo motors
def arm_normal_position():
    print('Arm will go to normal position\n')
    H1_sc.singleServo(12, -1, 1)
    H2_sc.singleServo(13, -1, 1)
    time.sleep(13)
    H1_sc.stopWiggle()
    H2_sc.stopWiggle()
    
    
    

# Calling all the functions in one
def test():

    arm_down()
    arm_gripper()
    arm_up()
    arm_normal_position()
    '''
    print('Arm will go down\n')
    H1_sc.singleServo(12, -1, 1)
    H2_sc.singleServo(13, -1, 1)
    time.sleep(7)
    H1_sc.stopWiggle()
    H2_sc.stopWiggle()
    
    print('Gripper will Grab the ball\n')
    G_sc.singleServo(15, 1, 1)
    time.sleep(3)
    G_sc.stopWiggle()
    
    print('Arm will go up\n')
    H1_sc.singleServo(12, 1, 3)
    H2_sc.singleServo(13, 1, 3)
    time.sleep(7)
    H1_sc.stopWiggle()
    H2_sc.stopWiggle()
    '''
    
    
if __name__ == '__main__':
    
    # Instance to initialise all servo to default position
    scGear = RPIservo.ServoCtrl()
    scGear.moveInit()
    
    # Instance to control pin 14 which is 4th motor
    P_sc = RPIservo.ServoCtrl()
    P_sc.start()
    
    # Instance to control pin 11 which is 1st motor
    T_sc = RPIservo.ServoCtrl()
    T_sc.start()
    
    # Instance to control pin 12 which is 2nd motor
    H1_sc = RPIservo.ServoCtrl()
    H1_sc.start()
    
    # Instance to control pin 13 which is 3rd motor
    H2_sc = RPIservo.ServoCtrl()
    H2_sc.start()
    
    # Instance to control pin 15 which is 5th motor(Gripper motor)
    G_sc = RPIservo.ServoCtrl()
    G_sc.start()
    
    time.sleep(1)
    test()
    ##time.sleep(0.09)
