from __future__ import print_function
import time
import math
#import serial
#from roboclaw import Roboclaw

""" verifies parsing and command prompt functionality so doesn't connect to rover / RCs / rasppi / etc
doesn't test validity of encoder values so 'read' values random & static 
prints which function and any specifics relative to that function"""

#constants (like #define in c)
RC1 = 0
RC2 = 1
RC3 = 2
RC4 = 3
RC5 = 4

# not necessary for Grover Team's testing purposes but will be implemented
# when user gets their hands on it
MAX_USER_SPEED = 100
MIN_USER_SPEED = 10
MIN_USER_TIME = 3
MAX_MASTER_SPEED = 127
MIN_MASTER_SPEED = 0    # full stop, 1-7 too slow for noteworthy movement

# rc = Roboclaw("/dev/ttyS0",115200)
# rc.Open()
# address = [0x80,0x81,0x82,0x83,0x84]	

# rc.ResetEncoders(address[RC1])
# rc.ResetEncoders(address[RC2])
# rc.ResetEncoders(address[RC3])
# rc.ResetEncoders(address[RC4])
# rc.ResetEncoders(address[RC5])

def check_valid_parameters(speed, timer):
    if(speed > MAX_USER_SPEED or speed < MIN_USER_SPEED):
        print("Error: invalid speed")
    
    if(timer < MIN_USER_TIME):
        print("Error: invalid time")
    return -1;

    
def print_grover(encoderArrayM1, encoderArrayM2, testName):
    print("Test: ", testName)
    print("\n\t   Roboclaw 1\t\t    Roboclaw 2")
    print('\t'.ljust(17, '_'),"\t     ______")
    print("Wheel:\t4\t       5\t\t6")
    print("    --------        --------\t    --------")
    print("    |{:6}|--\t    |{:6}|\t  --|{:6}|".format(encoderArrayM1[RC1],encoderArrayM2[RC1],encoderArrayM1[RC2]))
    print("    --------  |     --------\t |  --------")
    print("              |         |   \t |")
    print ('\t'.ljust(34, '-'))
    print("\t|\t\t\t\t|\n<--B(-)\t|\t\t\tGantry\t|  F(+)-->\n\t|\t\t\t\t|")
    print ('\t'.ljust(34, '-'))
    print("              |         |  \t |")
    print("    --------  |     --------\t |  --------")
    print("    |{:6}|--\t    |{:6}|\t  --|{:6}|".format(encoderArrayM2[RC3],encoderArrayM1[RC3],encoderArrayM2[RC2]))
    print("    --------        --------\t    --------")
    print("Wheel:\t9\t       8\t\t7")
    print('\t'.ljust(17, '_'),"\t     ______")
    print("\t   Roboclaw 3\t\t    Roboclaw 2\n")
    print ('-'.ljust(60, '-'),"\n")

# def ResetEncs():
	# rc.ResetEncoders(address[0])
	# rc.ResetEncoders(address[1])
	# rc.ResetEncoders(address[2])
    
# def getEnc(motorID):
	# if (motorID % 2 == 0):
		# command = rc.ReadEncM1
	# elif (motorID % 2 == 1):
		# command = rc.ReadEncM2
	# else:
		# print("MotorID error")
		# return
	# cmd = command(address[motorID])[1]
	# if motorID == 5:
		# cmd = cmd * -1
	# return cmd
    
# tells all motors to stop, direction does not matter since 0 is default stop
# for all roboclaw movement commnads
# invoke: kill or k
def kill_all():
    print('killed')
    return 0
    # rc.ForwardM1(address[RC1], 0)
	# rc.ForwardM2(address[RC1], 0)
	# rc.ForwardM1(address[RC2], 0)
	# rc.ForwardM2(address[RC2], 0)
	# rc.ForwardM1(address[RC3], 0)
	# rc.ForwardM2(address[RC3], 0)
    # rc.ForwardM1(address[RC4], 0)
	# rc.ForwardM2(address[RC4], 0)
	# rc.ForwardM1(address[RC5], 0)
	# rc.ForwardM2(address[RC5], 0)
    # return 0
    
# tells all wheels to spin forward at speed for timer seconds 
# 'forward' direction relative to the front of the rover
# invoke: [RAF] <speed> <timer> 
def roll_all_forward(speed, timer):
    speed = int(speed)
    timer = int(timer)
    dataM1 = []
    dataM2 = []
    # ResetEncs()
	# rc.ForwardM1(address[RC1], speed)
	# rc.ForwardM2(address[RC1], speed)
	# rc.ForwardM1(address[RC2], speed)
	# rc.ForwardM2(address[RC2], speed)
	# rc.ForwardM1(address[RC3], speed)
	# rc.ForwardM2(address[RC3], speed)
	# time.sleep(int(timer))
	# rc.ForwardM1(address[RC1], 0)
	# rc.ForwardM2(address[RC1], 0)
	# rc.ForwardM1(address[RC2], 0)
	# rc.ForwardM2(address[RC2], 0)
	# rc.ForwardM1(address[RC3], 0)
	# rc.ForwardM2(address[RC3], 0)
	# dataM1.append(rc.ReadEncM1(address[RC1])([1]))
    # dataM1.append(rc.ReadEncM1(address[RC2])([1]))
    # dataM1.append(rc.ReadEncM1(address[RC3])([1]))
    # dataM2.append(rc.ReadEncM2(address[RC1])([1]))
    # dataM2.append(rc.ReadEncM2(address[RC2])([1]))
    # dataM2.append(rc.ReadEncM2(address[RC3])([1]))
    print('roll all forward: {} for {} seconds'.format(speed, timer))

    # dummy values -> testing for parser
    dataM1.append(15234)
    dataM1.append(15128)
    dataM1.append(15689)
    dataM2.append(15444)
    dataM2.append(15093)
    dataM2.append(15230)

    print_grover(dataM1, dataM2, "test - All forward")

    return 0

    
# tells all wheels to spin backward at speed for timer seconds 
# 'backward' direction relative to the back of the rover
# invoke: [RAB] <speed> <timer> 
def roll_all_backward(speed, timer):
    speed = int(speed)
    timer = int(timer)
    dataM1 = []
    dataM2 = []
    # ResetEncs()
	# rc.BackwardM1(address[RC1], speed)
	# rc.BackwardM2(address[RC1], speed)
	# rc.BackwardM1(address[RC2], speed)
	# rc.BackwardM2(address[RC2], speed)
	# rc.BackwardM1(address[RC3], speed)
	# rc.BackwardM2(address[RC3], speed)
	# time.sleep(int(timer))
	# rc.BackwardM1(address[RC1], 0)
	# rc.BackwardM2(address[RC1], 0)
	# rc.BackwardM1(address[RC2], 0)
	# rc.BackwardM2(address[RC2], 0)
	# rc.BackwardM1(address[RC3], 0)
	# rc.BackwardM2(address[RC3], 0)
	# dataM1.append(rc.ReadEncM1(address[RC1])([1]))
    # dataM1.append(rc.ReadEncM1(address[RC2])([1]))
    # dataM1.append(rc.ReadEncM1(address[RC3])([1]))
    # dataM2.append(rc.ReadEncM2(address[RC1])([1]))
    # dataM2.append(rc.ReadEncM2(address[RC2])([1]))
    # dataM2.append(rc.ReadEncM2(address[RC3])([1]))
    print('roll all backward: {} for {} seconds'.format(speed, timer))

    dataM1.append(-15234)
    dataM1.append(-15128)
    dataM1.append(-15689)
    dataM2.append(-15444)
    dataM2.append(-15093)
    dataM2.append(-15230)

    print_grover(dataM1, dataM2, "test - All backward")
    return 0
    
# tests a roboclaw set specified by motorID at register speed for timer seconds
# which determines which test to run:
#   1 -> both forward
#   2 -> both backward
#   3 -> M1 forward, M2 backward
#   4 -> M1 backward, M2 forward
# to invoke: [RS] [motorID] [which] <speed> <timer>
def rotate_set(motorID, which, speed, timer):
    motorID = int(motorID)
    which = int(which)
    speed = int(speed)
    timer = int(timer)
    motorID -= 1
    #ResetEncs()
    if(which == 1):
        # rc.ForwardM1(address[motorID], speed)
        # rc.ForwardM2(address[motorID], speed)
        # time.sleep(int(timer))
        # rc.ForwardM1(address[motorID], 0)
        # rc.ForwardM2(address[motorID], 0)
        print('which: {} both forward'.format(which))
        
    elif(which == 2):
        # rc.BackwardM1(address[motorID], speed)
        # rc.BackwardM2(address[motorID], speed)
        # time.sleep(int(timer))
        # rc.BackwardM1(address[motorID], 0)
        # rc.BackwardM2(address[motorID], 0)
        print('which: {} both backward'.format(which))
        
    elif(which == 3):
        # rc.ForwardM1(address[motorID], speed)
        # rc.BackwardM2(address[motorID], speed)
        # time.sleep(int(timer))
        # rc.ForwardM1(address[motorID], 0)
        # rc.BackwardM2(address[motorID], 0)
        print('which: {} M1 forward, M2 backward'.format(which))
        
    elif(which == 4):
        # rc.BackwardM1(address[motorID], speed)
        # rc.ForwardM2(address[motorID], speed)
        # time.sleep(int(timer))
        # rc.BackwardM1(address[motorID], 0)
        # rc.ForwardM2(address[motorID], 0)
        print('which: {} M1 backward, M2 forward'.format(which))
        
    else:
        return -1
        
    #print('RC{}: M1 {} M2 {}'.format(motorID+1, rc.ReadEncM1(address[motorID])[1], rc.ReadEncM2(address[motorID])[1]))
    print('RC {}    speed: {}   timer: {}'.format(motorID+1, speed, timer))
    return 0
    
    
# rolls the individual wheel motor from RC motorID at speed for timer seconds
# can either be forwards (F or f) or backwards (B or b)
# to invoke: [RI] [motorID] [motor] [direction] <speed> <timer>
def rotate_individual_wheel(motorID, motor, direction, speed, timer):
    motorID = int(motorID)
    motor = int(motor)
    speed = int(speed)
    timer = int(timer)
    motorID -= 1
    result = 0
    # ResetEncs()
    if(direction == "F" or direction == "f"):
        if(motor == 1):
            # rc.ForwardM1(address[motorID], speed)
            # time.sleep(int(timer))
            # rc.ForwardM1(address[motorID], 0)
            # result = rc.ReadEncM1(address[motorID])[1]
            print('M1 forward')
        else:
            # rc.ForwardM2(address[motorID], speed)
            # time.sleep(int(timer))
            # rc.ForwardM2(address[motorID], 0)
            # result = rc.ReadEncM2(address[motorID])[1]
            print('M2 forward')

    elif(direction == "B" or direction == "b"):
        if(motor == 1):
            # rc.BackwardM1(address[motorID], speed)
            # time.sleep(int(timer))
            # rc.BackwardM1(address[motorID], 0)
            # result = rc.ReadEncM1(address[motorID])[1]
            print('M1 backward')
        else:
            # rc.BackwardM2(address[motorID], speed)
            # time.sleep(int(timer))
            # rc.BackwardM2(address[motorID], 0)
            # result = rc.ReadEncM2(address[motorID])[1]
            print('M2 backward')

    else:
        return -1

    #print('RC{} M{}: {}'.format(motorID, motor, result))
    print('RC: {}   result: {}'.format(motorID+1, 0))
    return 0

# turns all corner wheels right at speed for timer seconds or until it cannot turn anymore
# 'right' turn relative to the front of the rover
# IMPORTANT: don't force corner wheels to articulate past their stopping point
#   stopping point: TBD
# to invoke: [AAR] <speed> <timer>
def articulate_all_corners_right(speed, timer):
    speed = int(speed)
    timer = int(timer)
    dataM1 = []
    dataM2 = []
    # ResetEncs()
    # rc.ForwardM1(address[RC4], speed)
    # rc.ForwardM1(address[RC5], speed)
    # rc.ForwardM2(address[RC4], speed)
    # rc.ForwardM2(address[RC5], speed)
    # time.sleep(timer)
    # rc.ForwardM1(address[RC4], 0)
    # rc.ForwardM1(address[RC5], 0)
    # rc.ForwardM2(address[RC4], 0)
    # rc.ForwardM2(address[RC5], 0)
    # dataM1.append(rc.ReadEncM1(address[RC4])[1])
    # dataM1.append(0)                                    # left middle wheel
    # dataM1.append(rc.ReadEncM1(address[RC5])[1])
    # dataM1.append(rc.ReadEncM2(address[RC4])[1])
    # dataM1.append(0)                                    # right middle wheel
    # dataM1.append(rc.ReadEncM2(address[RC5])[1])
    print('articulate all right: {} for {} seconds'.format(speed, timer))

    dataM1.append(15234)
    dataM1.append(15128)
    dataM1.append(15689)
    dataM2.append(15444)
    dataM2.append(15093)
    dataM2.append(15230)

    print_grover(dataM1, dataM2, "test - Corner Articulation Right")
    return 0
    
    
# turns all corner wheels left at speed for timer seconds or until it cannot turn anymore
# 'left' turn relative to the back of the rover
# IMPORTANT: don't force corner wheels to articulate past their stopping point
#   stopping point: TBD
# to invoke: [AAL] <speed> <timer>
def articulate_all_corners_left(speed, timer):
    speed = int(speed)
    timer = int(timer)
    dataM1 = []
    dataM2 = []
    # ResetEncs()
    # rc.BackwardM1(address[RC4], speed)
    # rc.BackwardM1(address[RC5], speed)
    # rc.BackwardM2(address[RC4], speed)
    # rc.BackwardM2(address[RC5], speed)
    # time.sleep(timer)
    # rc.BackwardM1(address[RC4], 0)
    # rc.BackwardM1(address[RC5], 0)
    # rc.BackwardM2(address[RC4], 0)
    # rc.BackwardM2(address[RC5], 0)
    # dataM1.append(rc.ReadEncM1(address[RC4])[1])
    # dataM1.append(0)                                    # left middle wheel
    # dataM1.append(rc.ReadEncM1(address[RC5])[1])
    # dataM1.append(rc.ReadEncM2(address[RC4])[1])
    # dataM1.append(0)                                    # right middle wheel
    # dataM1.append(rc.ReadEncM2(address[RC5])[1])
    print('articulate all left: {} for {} seconds'.format(speed, timer))

    dataM1.append(-15234)
    dataM1.append(-15128)
    dataM1.append(-15689)
    dataM2.append(-15444)
    dataM2.append(-15093)
    dataM2.append(-15230)

    print_grover(dataM1, dataM2, "test - Corner Articulation Left")
    return 0