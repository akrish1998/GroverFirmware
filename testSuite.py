from __future__ import print_function
import time
import math
import serial
import unittest
from roboclaw import Roboclaw


#global for time stopper for seeing live encoder vals
stopper = 0

#constants (like #define in c): which RC corresponds to the address in the address list
RC1 = 0
RC2 = 1
RC3 = 2
RC4 = 3
RC5 = 4

#corner encoder motors cuz they're inverted
FR_CONTROLLER_MOTOR = 1
BR_CONTROLLER_MOTOR = 2
FL_CONTROLLER_MOTOR = 2
BL_CONTROLLER_MOTOR = 1

FR_ENC_MOTOR = 2
BR_ENC_MOTOR = 1
FL_ENC_MOTOR = 1
BL_ENC_MOTOR = 2

# corner enc values from calibration
FRONT_RIGHT = 0
BACK_RIGHT = 0
FRONT_LEFT = 0
BACK_LEFT = 0

#calibration parameters
FRONT_CALIBRATION_SPEED = 40
FRONT_SLOWER = 40
BACK_CALIBRATION_SPEED = 40
BACK_SLOWER = 40
CALIBRATION_TIME = 4
MAX_CORNER_ENC = 1550
INVALID_ENC = 1600

ARC_SPEED_FACTOR = 4			# when arc turning, outer wheel speed > inner wheel speed by 4x


rc = Roboclaw("/dev/ttyS0",115200)
rc.Open()
#0x80 -> 128 -> roboclaw #1 wheels 4 & 5 for wheel spin
#0x81 -> 129 -> roboclaw #2 wheels 6 & 7 for wheel spin
#0x82 -> 130 -> roboclaw #3 wheels 8 & 9 for wheel spin
#0x83 -> 131 -> roboclaw #4 wheels 4 & 6 for wheel rotation
#0x84 -> 132 -> roboclaw #5 wheels 7 & 9 for wheel rotation
address = [0x80,0x81,0x82,0x83,0x84]		

def cali_time_test():
	counter=0
	while(1):
		current_enc = rc.ReadEncM2(address[RC5])[1]
		time.sleep(0.1)
		print("enc: %s" % (current_enc))
	return 0

def getRegisterSpeed(speed):
	result2 = (0.002+speed) // 0.0009	# based on graph velocity formula for m/s
	return result2				# velo = 0.0009(reg value) - 0.002
    
    
def getTime(speed, dist):			# speed in m/s
	howLong = dist/speed			# velo = distance / time
	return howLong
	
def getVeloInMS(speed):				# converts register value to velocity in m/s
	msSpeed = (0.0009 * speed) - 0.002
	return msSpeed

def print_corner_enc():
	cornerEncoders = getCornerEncoders();
	print("Articulation encoders at startup:")
	print("Front left (RC4 M2): %s" % (cornerEncoders[1]))
	print("Front right (RC5 M1): %s" % (cornerEncoders[2]))
	print("Back left (RC4 M1): %s" % (cornerEncoders[0]))
	print("Back right (RC5 M2): %s" % (cornerEncoders[3]))


def calibrate_FR():
	global FRONT_RIGHT
	flag = 0
	left_most = 0
	right_most = 0
	centered = 0
	rc.BackwardM1(address[RC5], FRONT_CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM1(address[RC5], 0)
	left_most = rc.ReadEncM2(address[RC5])[1]
		
	rc.ForwardM1(address[RC5], FRONT_CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	#start = time.time()
	#while(time.time()-start<CALIBRATION_TIME):
		#if(rc.ReadEncM2(address[RC5])[1] >= 1500 and flag==0):		# not using 1550 cuz the enc values change fast, so giving it wide range
			#fr += MAX_CORNER_ENC
			#flag = 1
	
	rc.ForwardM1(address[RC5], 0)
	#fr += rc.ReadEncM2(address[RC5])[1]
	#fr = fr//2
	right_most = rc.ReadEncM2(address[RC5])[1]
	if(right_most <= left_most):
		right_most += MAX_CORNER_ENC
	center = (left_most+right_most)//2

	#if(fr >= INVALID_ENC):
		#fr -= MAX_CORNER_ENC
	
	#FRONT_RIGHT = fr;
	rc.BackwardM1(address[RC5], FRONT_SLOWER)
	while(1):
		if(center-100 <= rc.ReadEncM2(address[RC5])[1] <= center+100):	
			break
		time.sleep(0.25)
	rc.BackwardM1(address[RC5], 0)
	return 0

	
def calibrate_BR():
	global BACK_RIGHT
	flag = 0
	rc.BackwardM2(address[RC5], BACK_CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM2(address[RC5], 0)
	br = rc.ReadEncM1(address[RC5])[1]
		
	rc.ForwardM2(address[RC5], BACK_CALIBRATION_SPEED)
	start = time.time()
	while(time.time()-start<CALIBRATION_TIME):
		if(rc.ReadEncM1(address[RC5])[1] >= 1500 and flag==0):
			br += MAX_CORNER_ENC
			flag = 1
		time.sleep(0.1)

	rc.ForwardM2(address[RC5], 0)
	br += rc.ReadEncM1(address[RC5])[1]
	br = br//2
	if(br >= INVALID_ENC):
		br -= MAX_CORNER_ENC
		
	BACK_RIGHT = br
	print("br enc: %s" % (BACK_RIGHT))
	rc.BackwardM2(address[RC5], BACK_SLOWER)
	while(1):
		if(BACK_RIGHT-100 <= rc.ReadEncM1(address[RC5])[1] <= BACK_RIGHT+100):
			break
		time.sleep(0.25)
	rc.BackwardM2(address[RC5], 0)
	return 0
	
	
def calibrate_BL():
	global BACK_LEFT
	flag = 0
	left_most = 0
	right_most = 0
	centered = 0
	rc.BackwardM1(address[RC4], BACK_CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM1(address[RC4], 0)
	left_most = rc.ReadEncM2(address[RC4])[1]
		
	rc.ForwardM1(address[RC4], BACK_CALIBRATION_SPEED)
	#start = time.time()
	#while(time.time()-start<CALIBRATION_TIME):
		#if(rc.ReadEncM2(address[RC4])[1] >= 1500 and flag==0):		
			#bl += MAX_CORNER_ENC
			#flag = 1
		#time.sleep(0.1)
		#print("1st loop")

	rc.ForwardM1(address[RC4], 0)
	bl += rc.ReadEncM2(address[RC4])[1]
	bl = bl//2
	if(bl >= INVALID_ENC):
		bl -= MAX_CORNER_ENC
		
	BACK_LEFT = bl
	print("bl enc: %s" % (BACK_LEFT))
	rc.BackwardM1(address[RC4], BACK_SLOWER)
	while(1):
		if(BACK_LEFT-100 <= rc.ReadEncM2(address[RC4])[1] <= BACK_LEFT+100):
			break
		time.sleep(0.25)
		print("%s" % (rc.ReadEncM2(address[RC4])[1]))
	rc.BackwardM1(address[RC4], 0)
	return 0
	
	
def calibrate_FL():
	global FRONT_LEFT
	flag = 0
	left_most = 0
	right_most = 0
	centered = 0
	rc.BackwardM2(address[RC4], FRONT_CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM1(address[RC4], 0)
	left_most = rc.ReadEncM1(address[RC4])[1]
		
	rc.ForwardM2(address[RC4], FRONT_CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	#start = time.time()
	#while(time.time()-start<CALIBRATION_TIME+2):
		#if(rc.ReadEncM1(address[RC4])[1] >= 1500 and flag==0):		
			#fl += MAX_CORNER_ENC
			#flag = 1
		#time.sleep(0.1)

	rc.ForwardM2(address[RC4], 0)
	right_most = rc.ReadEncM1(address[RC4])[1]
	if(right_most <= left_most):
		right_most += MAX_CORNER_ENC
	centered = (left_most+right_most) // 2

	#fl += rc.ReadEncM1(address[RC4])[1]
	#fl = fl//2
	#if(fl >= INVALID_ENC):
		#fl -= MAX_CORNER_ENC
		
	#FRONT_LEFT = fl
	rc.BackwardM2(address[RC4], FRONT_SLOWER)
	while(1):
		if(centered-100 <= rc.ReadEncM1(address[RC4])[1] <= centered+100):
			break
		time.sleep(0.25)
	rc.BackwardM2(address[RC4], 0)
	return 0
	
	
# goes clockwise from front right
# remember motors inverted for turning & reading encs
def calibrate_corner_encoders():
	
	calibrate_FR()
	#calibrate_BR()
	#calibrate_BL()
	calibrate_FL()
	
	print("front right: %s   back right: %s    front left: %s   back left: %s" % (FRONT_RIGHT, BACK_RIGHT, FRONT_LEFT, BACK_LEFT))	
	return 0
	

	
# adrian's func, with slightly modified parameters 
def print_grover(encoderArrayM1, encoderArrayM2, testName):
	print("Test: ", testName)
	print("\n\t   Roboclaw 1\t\t    Roboclaw 2")
	print('\t'.ljust(17, '_'),"\t     ______")
	print("Wheel:\t4\t       5\t\t6")
	print("    --------        --------\t    --------")
	print("    |%6d|--\t    |%6d|\t  --|%6d|" %(encoderArrayM1[RC1],encoderArrayM2[RC1],encoderArrayM1[RC2]))
	print("    --------  |     --------\t |  --------")
	print("              |         |   \t |")
	print ('\t'.ljust(34, '-'))
	print("\t|\t\t\t\t|\n<--B(-)\t|\t\t\tGantry\t|  F(+)-->\n\t|\t\t\t\t|")
	print ('\t'.ljust(34, '-'))
	print("              |         |  \t |")
	print("    --------  |     --------\t |  --------")
	print("    |%6d|--\t    |%6d|\t  --|%6d|"%(encoderArrayM2[RC3],encoderArrayM1[RC3],encoderArrayM2[RC2]))
	print("    --------        --------\t    --------")
	print("Wheel:\t9\t       8\t\t7")
	print('\t'.ljust(17, '_'),"\t     ______")
	print("\t   Roboclaw 3\t\t    Roboclaw 2\n")
	print ('-'.ljust(60, '-'),"\n")
	return 0

	
def ResetEncs():
	rc.ResetEncoders(address[0])
	rc.ResetEncoders(address[1])
	rc.ResetEncoders(address[2])
	rc.ResetEncoders(address[3])
	rc.ResetEncoders(address[4])
	
def getCornerEncoders():
	values = []
	values.append(rc.ReadEncM1(address[RC4])[1])		# back left -> index 0
	values.append(rc.ReadEncM2(address[RC4])[1])		# front left -> index 1
	values.append(rc.ReadEncM1(address[RC5])[1])		# front right -> index 2
	values.append(rc.ReadEncM2(address[RC5])[1])		# back right -> index 3
	return values

	
def getEnc(motorID):
	if (motorID % 2 == 0):
		command = rc.ReadEncM1
	elif (motorID % 2 == 1):
		command = rc.ReadEncM2
	else:
		print("MotorID error")
		return -1
	cmd = command(address[motorID])[1]
	if motorID == 5:
		cmd = cmd * -1
	return cmd

	
# tells all motors to stop, direction does not matter since 0 is default stop
# for all roboclaw movement commnads
# invoke: kill or k
def kill_all():
	rc.ForwardM1(address[RC1], 0)
	rc.ForwardM2(address[RC1], 0)
	rc.ForwardM1(address[RC2], 0)
	rc.ForwardM2(address[RC2], 0)
	rc.ForwardM1(address[RC3], 0)
	rc.ForwardM2(address[RC3], 0)
	rc.ForwardM1(address[RC4], 0)
	rc.ForwardM2(address[RC4], 0)
	rc.ForwardM1(address[RC5], 0)
	rc.ForwardM2(address[RC5], 0)
	print("killed")
	return 0

	
# tells all wheels to spin forward at speed for timer seconds 
# 'forward' direction relative to the front of the rover
# invoke: [RAF] <speed?> <timer?> 
def roll_all_forward(speed, timer):
	speed = int(speed)
	timer = float(timer)
	dataM1 = []
	dataM2 = []
	#ResetEncs()
	rc.ForwardM1(address[RC1], speed)
	rc.ForwardM2(address[RC1], speed)
	rc.ForwardM1(address[RC2], speed)
	rc.ForwardM2(address[RC2], speed)
	rc.ForwardM1(address[RC3], speed)
	rc.ForwardM2(address[RC3], speed)
	time.sleep(int(timer))
	rc.ForwardM1(address[RC1], 0)
	rc.ForwardM2(address[RC1], 0)
	rc.ForwardM1(address[RC2], 0)
	rc.ForwardM2(address[RC2], 0)
	rc.ForwardM1(address[RC3], 0)
	rc.ForwardM2(address[RC3], 0)
	#kill_all()
	dataM1.append(rc.ReadEncM1(address[RC1])[1])
	dataM1.append(rc.ReadEncM1(address[RC2])[1])
	dataM1.append(rc.ReadEncM1(address[RC3])[1])
	dataM2.append(rc.ReadEncM2(address[RC1])[1])
	dataM2.append(rc.ReadEncM2(address[RC2])[1])
	dataM2.append(rc.ReadEncM2(address[RC3])[1])
	print_grover(dataM1, dataM2, "test - All forward")
	return 0

    
# tells all wheels to spin backward at speed for timer seconds 
# 'backward' direction relative to the back of the rover
# invoke: [RAB] <speed?> <timer?> 
def roll_all_backward(speed, timer):
	speed = int(speed)
	timer = float(timer)
	dataM1 = []
	dataM2 = []
	#ResetEncs()
	rc.BackwardM1(address[RC1], speed)
	rc.BackwardM2(address[RC1], speed)
	rc.BackwardM1(address[RC2], speed)
	rc.BackwardM2(address[RC2], speed)
	rc.BackwardM1(address[RC3], speed)
	rc.BackwardM2(address[RC3], speed)
	time.sleep(int(timer))
	rc.BackwardM1(address[RC1], 0)
	rc.BackwardM2(address[RC1], 0)
	rc.BackwardM1(address[RC2], 0)
	rc.BackwardM2(address[RC2], 0)
	rc.BackwardM1(address[RC3], 0)
	rc.BackwardM2(address[RC3], 0)
	#kill_all()
	dataM1.append(rc.ReadEncM1(address[RC1])[1])
	dataM1.append(rc.ReadEncM1(address[RC2])[1])
	dataM1.append(rc.ReadEncM1(address[RC3])[1])
	dataM2.append(rc.ReadEncM2(address[RC1])[1])
	dataM2.append(rc.ReadEncM2(address[RC2])[1])
	dataM2.append(rc.ReadEncM2(address[RC3])[1])
	print_grover(dataM1, dataM2, "test - All backward")
	return 0

	
# tests a roboclaw set specified by motorID at register speed for timer seconds
# which determines which test to run:
#   1 -> both forward
#   2 -> both backward
#   3 -> M1 forward, M2 backward
#   4 -> M1 backward, M2 forward
# to invoke: [RS] [motorID/RC?] [which/test?] <speed?> <timer?>
def rotate_set(motorID, which, speed, timer):
	motorID = int(motorID)
	which = int(which)
	speed = int(speed)
	timer = float(timer)
	motorID -= 1
	#ResetEncs()
	if(which == 1):                                 # both forward / right
		rc.ForwardM1(address[motorID], speed)
		rc.ForwardM2(address[motorID], speed)
		time.sleep(int(timer))
		rc.ForwardM1(address[motorID], 0)
		rc.ForwardM2(address[motorID], 0)
		print("test - Both forward")
        
	elif(which == 2):                               # both backward / left
		rc.BackwardM1(address[motorID], speed)
		rc.BackwardM2(address[motorID], speed)
		time.sleep(int(timer))
		rc.BackwardM1(address[motorID], 0)
		rc.BackwardM2(address[motorID], 0)
		print("test - Both backward")
        
	elif(which == 3):                               # M1 forward / right, M2 backward / left
		rc.ForwardM1(address[motorID], speed)
		rc.BackwardM2(address[motorID], speed)
		time.sleep(int(timer))
		rc.ForwardM1(address[motorID], 0)
		rc.BackwardM2(address[motorID], 0)
		print("test - M1 forward, M2 backward")
        
	elif(which == 4):                               # M1 backward / left, M2 forward / right
		rc.BackwardM1(address[motorID], speed)
		rc.ForwardM2(address[motorID], speed)
		time.sleep(int(timer))
		rc.BackwardM1(address[motorID], 0)
		rc.ForwardM2(address[motorID], 0)
		print("test - M1 backward, M2 forward")
        
	else:
		print("Invalid Input")
		return -1
        
	print("RC%s: M1 %s  M2 %s" % (rc.ReadEncM1(address[motorID])[1], rc.ReadEncM2(address[motorID])[1]))
	return 0
    
    
# rotates the individual wheel motor from RC motorID at speed for timer seconds
# can either be forwards (F or f) or backwards (B or b)
# to invoke: [RI] [motorID/RC?] [motor/wheel?] [direction?] <speed?> <timer?>
def rotate_individual_wheel(motorID, motor, direction, speed, timer):
	motorID = int(motorID)
	motor = int(motor)
	speed = int(speed)
	timer = float(timer)
	motorID -= 1
	result = 0
	#ResetEncs()
	if(direction == "F" or direction == "f"):
		if(motor == 1):                                         # M1 forward / right
			start = time.time()
			rc.ForwardM1(address[motorID], speed)
			time.sleep(int(timer))
			rc.ForwardM1(address[motorID], 0)
			stop = time.time() - start
			result = rc.ReadEncM1(address[motorID])[1]
			print("test - M1 forward")
		else:                             
			start = time.time()                      # M2 forward / right
			rc.ForwardM2(address[motorID], speed)
			time.sleep(int(timer))
			rc.ForwardM2(address[motorID], 0)
			stop = time.time() - start
			result = rc.ReadEncM2(address[motorID])[1]
			print("test - M2 forward")
    
	elif(direction == "B" or direction == "b"):     
		if(motor == 1):                                         # M1 backward / left
			start = time.time()
			rc.BackwardM1(address[motorID], speed)
			time.sleep(int(timer))
			rc.BackwardM1(address[motorID], 0)
			stop = time.time() - start
			result = rc.ReadEncM1(address[motorID])[1]
			print("test - M1 backward")
		else:                                                   # M2 backward / left
			start = time.time()
			rc.BackwardM2(address[motorID], speed)
			time.sleep(int(timer))
			rc.BackwardM2(address[motorID], 0)
			stop = time.time() - start
			result = rc.ReadEncM2(address[motorID])[1]
			print("test - M2 backward")
    
	else:
		print("Invalid Input")
		return -1

	print("RC%s M%s:  %s    time: %s" % (motorID+1, motor, result, stop))
	return 0

	
# turns all corner wheels right at speed for timer seconds or until it cannot turn anymore
# 'right' turn relative to the front of the rover
# IMPORTANT: don't force corner wheels to articulate past their stopping point
#   stopping point: TBD
# to invoke: [AAR] <speed?> <timer?>
def articulate_all_corners_right(speed, timer):
	speed = int(speed)
	timer = float(timer)
	dataM1 = []
	dataM2 = []
	#ResetEncs()
	rc.ForwardM1(address[RC4], speed)
	rc.ForwardM1(address[RC5], speed)
	rc.ForwardM2(address[RC4], speed)
	rc.ForwardM2(address[RC5], speed)
	time.sleep(timer)
	rc.ForwardM1(address[RC4], 0)
	rc.ForwardM1(address[RC5], 0)
	rc.ForwardM2(address[RC4], 0)
	rc.ForwardM2(address[RC5], 0)
	#kill_all()
	dataM1.append(rc.ReadEncM1(address[RC4])[1])
	dataM1.append(0)                                    # left middle wheel
	dataM1.append(rc.ReadEncM1(address[RC5])[1])
	dataM1.append(rc.ReadEncM2(address[RC4])[1])
	dataM1.append(0)                                    # right middle wheel
	dataM1.append(rc.ReadEncM2(address[RC5])[1])
	print_grover(dataM1, dataM2, "test - Corner Articulation Right (forward)")
	return 0
    
    
# turns all corner wheels left at speed for timer seconds or until it cannot turn anymore
# 'left' turn relative to the back of the rover
# IMPORTANT: don't force corner wheels to articulate past their stopping point
#   stopping point: TBD
# to invoke: [AAL] <speed?> <timer?>
def articulate_all_corners_left(speed, timer):
	speed = int(speed)
	timer = float(timer)
	dataM1 = []
	dataM2 = []
	#ResetEncs()
	rc.BackwardM1(address[RC4], speed)
	rc.BackwardM1(address[RC5], speed)
	rc.BackwardM2(address[RC4], speed)
	rc.BackwardM2(address[RC5], speed)
	time.sleep(timer)
	rc.BackwardM1(address[RC4], 0)
	rc.BackwardM1(address[RC5], 0)
	rc.BackwardM2(address[RC4], 0)
	rc.BackwardM2(address[RC5], 0)
	#kill_all()
	dataM1.append(rc.ReadEncM1(address[RC4])[1])
	dataM1.append(0)                                    # left middle wheel
	dataM1.append(rc.ReadEncM1(address[RC5])[1])
	dataM1.append(rc.ReadEncM2(address[RC4])[1])
	dataM1.append(0)                                    # right middle wheel
	dataM1.append(rc.ReadEncM2(address[RC5])[1])
	#print_grover(dataM1, dataM2, "test - Corner Articulation Left (backward)")
	return 0

	
def turn_calibration(speed, distance):
	outer_speed = float(speed)			# drive speed, not articulation speed, for outer wheels
	outer_reg_speed = getRegisterSpeed(outer_speed)
	inner_speed = outer_speed//ARC_SPEED_FACTOR
	inner_reg_speed = getRegisterSpeed(inner_speed)
	dist = float(distance)
	timer = getTime(outer_speed, dist)
	if(outer_speed>0.1123):
		print("slow down there bud")
		return 0
	
	
# to turn right, front wheels articulated right and back wheels articulated left
def full_turn_right(speed, dist):
	rc.ForwardM1(address[RC5], RC5M1_CORNER_SPEED)	#front right wheel
	rc.BackwardM2(address[RC5], CALIBRATION_SPEED)	#back right wheel
	rc.BackwardM1(address[RC4], CALIBRATION_SPEED)	#back left wheel
	rc.ForwardM2(address[RC4], CALIBRATION_SPEED)	#front left wheel
	time.sleep(CALIBRATION_TIME)
	rc.ForwardM1(address[RC5], 0)	#front right wheel
	rc.BackwardM2(address[RC5], 0)	#back right wheel
	rc.BackwardM1(address[RC4], 0)	#back left wheel
	rc.ForwardM2(address[RC4], 0)
	forward(speed, dist, 'r')
	return 0
	
# to turn left, front wheels articulated left and back wheels articulated right
def full_turn_left(speed, dist):
	rc.BackwardM1(address[RC5], RC5M1_CORNER_SPEED)	#front right wheel
	rc.ForwardM2(address[RC5], CALIBRATION_SPEED)	#back right wheel
	rc.ForwardM1(address[RC4], CALIBRATION_SPEED)	#back left wheel
	rc.BackwardM2(address[RC4], CALIBRATION_SPEED)	#front left wheel
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM1(address[RC5], 0)	#front right wheel
	rc.ForwardM2(address[RC5], 0)	#back right wheel
	rc.ForwardM1(address[RC4], 0)	#back left wheel
	rc.BackwardM2(address[RC4], 0)
	forward(speed, dist, 'l')
	return 0
	
	

def forward(speed, distance, direction):
	outer_speed = float(speed)			# drive speed, not articulation speed, for outer wheels
	outer_reg_speed = getRegisterSpeed(outer_speed)
	inner_speed = outer_speed//ARC_SPEED_FACTOR
	inner_reg_speed = getRegisterSpeed(inner_speed)
	dist = float(distance)
	timer = getTime(outer_speed, dist)
	if(outer_speed>0.1123):
		print("slow down there bud")
		return 0
	
	if (direction=='r'):					# left wheel speed (outer wheels) > right wheel speed (inner wheels)
		rc.ForwardM1(address[RC1], outer_reg_speed)		# left wheels, outer wheels
		rc.ForwardM2(address[RC1], outer_reg_speed)
		rc.ForwardM1(address[RC2], outer_reg_speed)
		rc.ForwardM2(address[RC2], inner_reg_speed)		# right wheels, inner wheels
		rc.ForwardM1(address[RC3], inner_reg_speed)
		rc.ForwardM2(address[RC3], inner_reg_speed)
		time.sleep(timer)
		rc.ForwardM1(address[RC1], 0)		# left wheels, outer wheels
		rc.ForwardM2(address[RC1], 0)
		rc.ForwardM1(address[RC2], 0)
		rc.ForwardM2(address[RC2], 0)		# right wheels, inner wheels
		rc.ForwardM1(address[RC3], 0)
		rc.ForwardM2(address[RC3], 0)
		
	elif(direction=='l'):					# right wheel speed (outer wheels) > left wheel speed (inner wheels)
		rc.ForwardM1(address[RC1], inner_reg_speed)		# left wheels, inner wheels
		rc.ForwardM2(address[RC1], inner_reg_speed)
		rc.ForwardM1(address[RC2], inner_reg_speed)
		rc.ForwardM2(address[RC2], outer_reg_speed)		# right wheels, outer wheels
		rc.ForwardM1(address[RC3], outer_reg_speed)
		rc.ForwardM2(address[RC3], outer_reg_speed)
		time.sleep(timer)
		rc.ForwardM1(address[RC1], 0)		# left wheels, outer wheels
		rc.ForwardM2(address[RC1], 0)
		rc.ForwardM1(address[RC2], 0)
		rc.ForwardM2(address[RC2], 0)		# right wheels, inner wheels
		rc.ForwardM1(address[RC3], 0)
		rc.ForwardM2(address[RC3], 0)
		
	else:						# straight forward / not arc turn
		rc.ForwardM1(address[RC1], outer_reg_speed)		# left wheels
		rc.ForwardM2(address[RC1], outer_reg_speed)
		rc.ForwardM1(address[RC2], outer_reg_speed)
		rc.ForwardM2(address[RC2], outer_reg_speed)		# right wheels
		rc.ForwardM1(address[RC3], outer_reg_speed)
		rc.ForwardM2(address[RC3], outer_reg_speed)
		time.sleep(timer)
		rc.ForwardM1(address[RC1], 0)
		rc.ForwardM2(address[RC1], 0)
		rc.ForwardM1(address[RC2], 0)
		rc.ForwardM2(address[RC2], 0)		
		rc.ForwardM1(address[RC3], 0)
		rc.ForwardM2(address[RC3], 0)
		
	return 0

