import RPIservo
import time



def test():


    print('Servo of gripper will rotate forward\n')
    H1_sc.singleServo(12, -1, 2)
    H2_sc.singleServo(13, -1, 2)
    ##time.sleep(1)
    H1.stopWiggle()
    H2.stopWiggle()
    
    '''
    print('servo will rotate backward\n')
    sc.singleServo(5, -1, 2)
    time.sleep(1)
    sc.stopWiggle()
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

    ###test()
    ##time.sleep(0.09)
