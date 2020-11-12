import RPIservo
import time



def test():


    print('Servo of gripper will rotate forward\n')
    sc.singleServo(15, 1, 1)
    time.sleep(1)
    sc.stopWiggle()
    
    '''
    print('servo will rotate backward\n')
    sc.singleServo(5, -1, 2)
    time.sleep(1)
    sc.stopWiggle()
    '''
    
if __name__ == '__main__':
    
    sc = RPIservo.ServoCtrl()
    sc.start()
    sc.moveServoInit([15])#test()