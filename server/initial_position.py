import RPIservo
import time

def arm_normal_position():
    print('Arm will go to normal position\n')
    H1_sc.singleServo(12, -1, 1)
    H2_sc.singleServo(13, -1, 1)
    time.sleep(13)
    H1_sc.stopWiggle()
    H2_sc.stopWiggle()
    
    
    
if __name__ == '__main__':
    # Instance to control pin 12 which is 2nd motor
    H1_sc = RPIservo.ServoCtrl()
    H1_sc.start()
    
    # Instance to control pin 13 which is 3rd motor
    H2_sc = RPIservo.ServoCtrl()
    H2_sc.start()
    
    arm_normal_position()
    
    

