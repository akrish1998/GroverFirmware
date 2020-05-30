from __future__ import print_function
import time
import math
import serial
import unittest
from roboclaw import Roboclaw

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
FR_CENTER = 0
FR_LEFT = 0
FR_RIGHT = 0
FR_CENTER_RAW = 0
FR_RIGHT_RAW = 0
FR_TOTAL = 0
FR_FACTOR = 0

BR_CENTER = 0
BR_LEFT = 0
BR_RIGHT = 0
BR_CENTER_RAW = 0
BR_RIGHT_RAW = 0
BR_TOTAL = 0
BR_FACTOR = 0

FL_CENTER = 0
FL_LEFT = 0
FL_RIGHT = 0
FL_CENTER_RAW = 0
FL_RIGHT_RAW = 0
FL_TOTAL = 0
FL_FACTOR = 0

BL_CENTER = 0
BL_LEFT = 0
BL_RIGHT = 0
BL_CENTER_RAW = 0
BL_RIGHT_RAW = 0
BL_TOTAL = 0
BL_FACTOR = 0

#calibration parameters
CALIBRATION_SPEED = 40
CALIBRATION_TIME = 4
MAX_CORNER_ENC = 1550
INVALID_ENC = 1600

# arc turn constants
ARC_SPEED_FACTOR = 4			# when arc turning, outer wheel speed > inner wheel speed by 4x in m/s
R_OUTER = 0.32				# 320 mm dist between corner wheels	
R_HEIGHT = 0.29
MAX_TURN = 36

rc = Roboclaw("/dev/ttyS0",115200)
rc.Open()
#0x80 -> 128 -> roboclaw #1 wheels 4 & 5 for wheel spin
#0x81 -> 129 -> roboclaw #2 wheels 6 & 7 for wheel spin
#0x82 -> 130 -> roboclaw #3 wheels 8 & 9 for wheel spin
#0x83 -> 131 -> roboclaw #4 wheels 4 & 6 for wheel rotation
#0x84 -> 132 -> roboclaw #5 wheels 7 & 9 for wheel rotation
address = [0x80,0x81,0x82,0x83,0x84]		

def get_register_speed(speed):
	result2 = (0.002+speed) // 0.0009	# based on graph velocity formula for m/s
	return result2				# velo = 0.0009(reg value) - 0.002
    
    
def get_time(speed, dist):			# speed in m/s
	howLong = dist/speed			# velo = distance / time
	return howLong
	
def get_velo_ms(speed):				# converts register value to velocity in m/s
	msSpeed = (0.0009 * speed) - 0.002
	return msSpeed
	
def get_enc_by_degree(direction, degree, raw_center, wheel_factor):
	deg = int(degree)
	if(direction=='left'):
		deg = deg * -1
		
	enc = int(wheel_factor * deg + raw_center)
	if(enc > MAX_CORNER_ENC):
		enc = enc - MAX_CORNER_ENC
	print("degree -> enc: %s" % (enc))
	return enc
	
# value is the read encoder value, no wheel differientiating done here just calculations
def get_degree_by_enc(value, wheel_factor, raw_right, raw_center):
	val = int(value)
	if(value + MAX_CORNER_ENC < raw_right):
		val = val + MAX_CORNER_ENC
	
	deg = (val - raw_center) // wheel_factor
	print("end -> degree: %s" % (deg))
	return deg
	
	
def get_inner_velo(degree, outer_speed):
	deg = int(degree)
	
	if(deg > MAX_TURN):
		print("Invalid Angle")
		return -1
	
	outer_velo = float(outer_speed)
	percent_diff = 0.9875*(math.exp(-0.016*deg))
	inner_velo = percent_diff*outer_velo
	print("outer: %s   inner: %s" % (outer_velo, round(inner_velo, 4)))
	#print(outer_reg, inner_reg)
	return inner_velo

	
def get_arc_time(degree, inner_speed):
	deg = int(degree)
	
	if(deg > MAX_TURN):
		print("Invalid Angle")
		return -1
	
	rad = math.radians(deg)
	velo = float(inner_speed)
	inner_dist = R_HEIGHT/(math.tan(rad))
	arc_time = (rad*inner_dist) / velo
	print("arc time: %s" % (arc_time))
	return arc_time


def calibrate_FR():
	print("FR")
	global FR_CENTER
	global FR_LEFT
	global FR_RIGHT
	global FR_CENTER_RAW
	global FR_TOTAL
	
	flag = 0
	left_most = 0
	right_most = 0
	centered = 0

	rc.BackwardM1(address[RC5], CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM1(address[RC5], 0)
	left_most = rc.ReadEncM2(address[RC5])[1]
	FR_LEFT = left_most

	rc.ForwardM1(address[RC5], CALIBRATION_SPEED)
	start = time.time()
	while(time.time()-start<CALIBRATION_TIME):
		if(rc.ReadEncM2(address[RC5])[1] >= 1500 and flag==0):		# not using 1550 cuz the enc values change fast, so giving it wide range
			centered += MAX_CORNER_ENC
			flag = 1
	
	rc.ForwardM1(address[RC5], 0)
	right_most = rc.ReadEncM2(address[RC5])[1]
	FR_RIGHT = right_most
	centered += right_most
	FR_TOTAL = centered
	centered = (centered+left_most)//2
	FR_CENTER_RAW = centered

	if(centered >= INVALID_ENC):
		centered -= MAX_CORNER_ENC

	FR_CENTER = centered
	print("center: %s" % (centered))
	rc.BackwardM1(address[RC5], CALIBRATION_SPEED)
	while(1):
		if(centered-100 <= rc.ReadEncM2(address[RC5])[1] <= centered+100):	
			break
		print(rc.ReadEncM2(address[RC5])[1])
		time.sleep(0.2)
	rc.BackwardM1(address[RC5], 0)

	return 0


def calibrate_BR():
	print("BR")
	global BR_CENTER
	global BR_LEFT
	global BR_RIGHT
	global BR_CENTER_RAW
	global BR_TOTAL

	flag = 0
	left_most = 0
	right_most = 0
	centered = 0

	rc.BackwardM2(address[RC5], CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM2(address[RC5], 0)
	left_most = rc.ReadEncM1(address[RC5])[1]
	BR_LEFT = left_most

	rc.ForwardM2(address[RC5], CALIBRATION_SPEED)
	start = time.time()
	while(time.time()-start<CALIBRATION_TIME):
		if(rc.ReadEncM1(address[RC5])[1] >= 1500 and flag==0):
			centered += MAX_CORNER_ENC
			flag = 1
		time.sleep(0.1)

	rc.ForwardM2(address[RC5], 0)
	right_most = rc.ReadEncM1(address[RC5])[1]
	BR_RIGHT = right_most
	centered += right_most
	BR_TOTAL = centered
	centered = (centered+left_most) // 2
	BR_CENTER_RAW = centered

	if(centered >= INVALID_ENC):
		centered -= MAX_CORNER_ENC

	BR_CENTER = centered
	print("center: %s"%(centered))
	rc.BackwardM2(address[RC5], CALIBRATION_SPEED)
	while(1):
		if(centered-100 <= rc.ReadEncM1(address[RC5])[1] <= centered+100):
			break
		print(rc.ReadEncM1(address[RC5])[1])
		time.sleep(0.2)
	rc.BackwardM2(address[RC5], 0)

	return 0
	
	
def calibrate_BL():
	print("BL")
	global BL_CENTER
	global BL_LEFT
	global BL_RIGHT
	global BL_CENTER_RAW 
	global BL_TOTAL
	
	flag = 0
	left_most = 0
	right_most = 0
	centered = 0
	
	rc.BackwardM1(address[RC4], CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM1(address[RC4], 0)
	left_most = rc.ReadEncM2(address[RC4])[1]
	BL_LEFT = left_most

	rc.ForwardM1(address[RC4], CALIBRATION_SPEED)
	start = time.time()
	while(time.time()-start<CALIBRATION_TIME):
		if(rc.ReadEncM2(address[RC4])[1] >= 1500 and flag==0):		
			centered += MAX_CORNER_ENC
			flag = 1
		time.sleep(0.1)

	rc.ForwardM1(address[RC4], 0)
	right_most = rc.ReadEncM2(address[RC4])[1]
	BL_RIGHT = right_most
	centered += right_most
	BL_TOTAL = centered
	centered = (centered+left_most) // 2
	BL_CENTER_RAW = centered
	
	if(centered >= INVALID_ENC):
		centered -= MAX_CORNER_ENC

	BL_CENTER = centered
	print("center: %s" % (centered))
	rc.BackwardM1(address[RC4], CALIBRATION_SPEED)
	while(1):
		if(centered-100 <= rc.ReadEncM2(address[RC4])[1] <= centered+100):
			break
		print(rc.ReadEncM2(address[RC4])[1])
		time.sleep(0.2)
	rc.BackwardM1(address[RC4], 0)

	return 0
	
	
def calibrate_FL():
	print("FL")
	global FL_CENTER
	global FL_LEFT
	global FL_RIGHT
	global FL_CENTER_RAW 
	global FL_TOTAL
	
	flag = 0
	left_most = 0
	right_most = 0
	centered = 0
	
	rc.BackwardM2(address[RC4], CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM1(address[RC4], 0)
	left_most = rc.ReadEncM1(address[RC4])[1]
	FL_LEFT = left_most

	rc.ForwardM2(address[RC4], CALIBRATION_SPEED)
	start = time.time()
	while(time.time()-start<CALIBRATION_TIME):
		if(rc.ReadEncM1(address[RC4])[1] >= 1500 and flag==0):		
			centered += MAX_CORNER_ENC
			flag = 1
		time.sleep(0.1)

	rc.ForwardM2(address[RC4], 0)
	right_most = rc.ReadEncM1(address[RC4])[1]
	FL_RIGHT = right_most
	centered += right_most
	FL_TOTAL = centered
	centered = (centered + left_most) // 2
	FL_CENTER_RAW = centered

	if(centered >= INVALID_ENC):
		centered -= MAX_CORNER_ENC

	FL_CENTER = centered
	print("center: %s" % (centered))
	rc.BackwardM2(address[RC4], CALIBRATION_SPEED)
	while(1):
		if(centered-100 <= rc.ReadEncM1(address[RC4])[1] <= centered+100):
			break
		print(rc.ReadEncM1(address[RC4])[1])
		time.sleep(0.2)
	rc.BackwardM2(address[RC4], 0)

	return 0
	
	
# goes clockwise from front right
# remember motors inverted for turning & reading encs
def calibrate_corner_encoders():
	calibrate_FR()
	calibrate_BR()
	calibrate_BL()
	calibrate_FL()
	calculate_wheel_factor()
	return 0

	
def ResetEncs():
	rc.ResetEncoders(address[0])
	rc.ResetEncoders(address[1])
	rc.ResetEncoders(address[2])
	rc.ResetEncoders(address[3])
	rc.ResetEncoders(address[4])
	
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
	return 0

	
	
	
def articulate_FR(direction, speed, degree):
	global FR_CENTER
	global FR_CENTER_RAW
	global FR_FACTOR
	global FR_RIGHT_RAW
	
	outer_velo = float(speed)
	deg = int(degree)
	encoder_val = get_enc_by_degree(direction, deg, FR_CENTER_RAW, FR_FACTOR)
	current_position = rc.ReadEncM2(address[RC5])[1]
	current_position = get_degree_by_enc(current_position, FR_FACTOR, FR_RIGHT_RAW, FR_CENTER_RAW)
	
	if(current_position < deg):		# turn right
		rc.ForwardM1(address[RC5], CALIBRATION_SPEED)
		while(1):
			if(encoder_val-100 <= rc.ReadEncM2(address[RC5])[1] <= encoder_val+100):
				break
			time.sleep(0.25)
		rc.ForwardM1(address[RC5], 0)

	elif(current_position > deg):		# turn left
		rc.BackwardM1(address[RC5], CALIBRATION_SPEED)
		while(1):
			if(encoder_val-100 <= rc.ReadEncM2(address[RC5])[1] <= encoder_val+100):
				break
			time.sleep(0.25)
		rc.BackwardM1(address[RC5], 0)
	return 0
	
	
def articulate_BR(direction, speed, degree):
	global BR_CENTER
	global BR_CENTER_RAW
	global BR_FACTOR
	global BR_RIGHT_RAW
	
	outer_velo = float(speed)
	deg = int(degree)
	encoder_val = get_enc_by_degree(direction, deg, BR_CENTER_RAW, BR_FACTOR)
	current_position = rc.ReadEncM1(address[RC5])[1]
	current_position = get_degree_by_enc(current_position, BR_FACTOR, BR_RIGHT_RAW, BR_CENTER_RAW)
	
	if(current_position < deg):		# turn right
		rc.ForwardM2(address[RC5], CALIBRATION_SPEED)
		while(1):
			if(encoder_val-100 <= rc.ReadEncM1(address[RC5])[1] <= encoder_val+100):
				break
			time.sleep(0.25)
		rc.ForwardM2(address[RC5], 0)

	elif(current_position > deg):		# turn left
		rc.BackwardM2(address[RC5], CALIBRATION_SPEED)
		while(1):
			if(encoder_val-100 <= rc.ReadEncM1(address[RC5])[1] <= encoder_val+100):
				break
			time.sleep(0.25)
		rc.BackwardM2(address[RC5], 0)
	return 0
	
	
def articulate_FL(direction, speed, degree):
	global FL_CENTER
	global FL_CENTER_RAW
	global FL_FACTOR
	global FL_RIGHT_RAW
	
	outer_velo = float(speed)
	deg = int(degree)
	encoder_val = get_enc_by_degree(direction, deg, FL_CENTER_RAW, FL_FACTOR)
	current_position = rc.ReadEncM1(address[RC4])[1]
	current_position = get_degree_by_enc(current_position, FL_FACTOR, FL_RIGHT_RAW, FL_CENTER_RAW)
	
	if(current_position < deg):		# turn right
		rc.ForwardM2(address[RC4], CALIBRATION_SPEED)
		while(1):
			if(encoder_val-100 <= rc.ReadEncM1(address[RC4])[1] <= encoder_val+100):
				break
			time.sleep(0.25)
		rc.ForwardM2(address[RC4], 0)

	elif(current_position > deg):		# turn left
		rc.BackwardM2(address[RC4], CALIBRATION_SPEED)
		while(1):
			if(encoder_val-100 <= rc.ReadEncM1(address[RC4])[1] <= encoder_val+100):
				break
			time.sleep(0.25)
		rc.BackwardM2(address[RC4], 0)
	return 0
	
	
def articulate_BL(direction, speed, degree):
	global BL_CENTER
	global BL_CENTER_RAW
	global BL_FACTOR
	global BL_RIGHT_RAW
	
	outer_velo = float(speed)
	deg = int(degree)
	encoder_val = get_enc_by_degree(direction, deg, BL_CENTER_RAW, BL_FACTOR)
	current_position = rc.ReadEncM2(address[RC4])[1]
	current_position = get_degree_by_enc(current_position, BL_FACTOR, BL_RIGHT_RAW, BL_CENTER_RAW)
	
	if(current_position < deg):		# turn right
		rc.ForwardM1(address[RC4], CALIBRATION_SPEED)
		while(1):
			if(encoder_val-100 <= rc.ReadEncM2(address[RC4])[1] <= encoder_val+100):
				break
			time.sleep(0.25)
		rc.ForwardM1(address[RC4], 0)

	elif(current_position > deg):		# turn left
		rc.BackwardM1(address[RC4], CALIBRATION_SPEED)
		while(1):
			if(encoder_val-100 <= rc.ReadEncM2(address[RC4])[1] <= encoder_val+100):
				break
			time.sleep(0.25)
		rc.BackwardM1(address[RC4], 0)
	return 0
		
	
# tells all wheels to spin forward at speed for timer seconds 
# 'forward' direction relative to the front of the rover
# invoke: [RAF] <speed?> <timer?> 
def roll_all_forward(speed, timer):
	speed = int(speed)
	timer = float(timer)
	
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

	return 0

    
# tells all wheels to spin backward at speed for timer seconds 
# 'backward' direction relative to the back of the rover
# invoke: [RAB] <speed?> <timer?> 
def roll_all_backward(speed, timer):
	speed = int(speed)
	timer = float(timer)

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
	
	return 0
	
# turns all corner wheels right at speed for timer seconds or until it cannot turn anymore
# 'right' turn relative to the front of the rover
# IMPORTANT: don't force corner wheels to articulate past their stopping point
#   stopping point: TBD
# to invoke: [AAR] <speed?> <timer?>
def articulate_all_corners_right(speed, timer):
	speed = int(speed)
	timer = float(timer)

	rc.ForwardM1(address[RC4], speed)
	rc.ForwardM1(address[RC5], speed)
	rc.ForwardM2(address[RC4], speed)
	rc.ForwardM2(address[RC5], speed)
	time.sleep(timer)
	rc.ForwardM1(address[RC4], 0)
	rc.ForwardM1(address[RC5], 0)
	rc.ForwardM2(address[RC4], 0)
	rc.ForwardM2(address[RC5], 0)

	return 0
    
    
# turns all corner wheels left at speed for timer seconds or until it cannot turn anymore
# 'left' turn relative to the back of the rover
# IMPORTANT: don't force corner wheels to articulate past their stopping point
#   stopping point: TBD
# to invoke: [AAL] <speed?> <timer?>
def articulate_all_corners_left(speed, timer):
	speed = int(speed)
	timer = float(timer)

	rc.BackwardM1(address[RC4], speed)
	rc.BackwardM1(address[RC5], speed)
	rc.BackwardM2(address[RC4], speed)
	rc.BackwardM2(address[RC5], speed)
	time.sleep(timer)
	rc.BackwardM1(address[RC4], 0)
	rc.BackwardM1(address[RC5], 0)
	rc.BackwardM2(address[RC4], 0)
	rc.BackwardM2(address[RC5], 0)

	return 0
	
	
# to turn right, front wheels articulated right and back wheels articulated left
def turn_right(speed, degree):
	articulate_FR('right', speed, degree)
	articulate_BR('right', speed, degree)
	articulate_FL('right', speed, degree)
	articulate_BL('right', speed, degree)
	
	outer_speed = float(speed)
	inner_speed = get_inner_velo(degree, outer_speed)
	inner_speed_reg = get_register_speed(inner_speed)
	outer_speed_reg = get_register_speed(outer_speed)
	the_time = get_arc_time(degree, inner_speed)
	forward(outer_speed_reg, inner_speed_reg, the_time, 'right')
	
	return 0
	
# to turn left, front wheels articulated left and back wheels articulated right
def turn_left(speed, degree):
	articulate_FR('left', speed, degree)
	articulate_BR('left', speed, degree)
	articulate_FL('left', speed, degree)
	articulate_BL('left', speed, degree)
	
	outer_speed = float(speed)
	inner_speed = get_inner_velo(degree, outer_speed)
	inner_speed_reg = get_register_speed(inner_speed)
	outer_speed_reg = get_register_speed(outer_speed)
	the_time = get_arc_time(degree, inner_speed)
	forward(outer_speed_reg, inner_speed_reg, the_time, 'left')
	
	return 0
	
	

def forward(outer_speed, inner_speed, the_time, direction):
	outer = int(outer_speed)
	inner = int(inner_speed)
	timer = float(the_time)
	
	if(direction=='right'):				# right inner, left outer
		rc.ForwardM1(address[RC1], outer)
		rc.ForwardM2(address[RC1], outer)
		rc.ForwardM1(address[RC2], outer)
		rc.ForwardM2(address[RC2], inner)
		rc.ForwardM1(address[RC3], inner)
		rc.ForwardM2(address[RC3], inner)
		time.sleep(int(timer))
		rc.ForwardM1(address[RC1], 0)
		rc.ForwardM2(address[RC1], 0)
		rc.ForwardM1(address[RC2], 0)
		rc.ForwardM2(address[RC2], 0)
		rc.ForwardM1(address[RC3], 0)
		rc.ForwardM2(address[RC3], 0)
	else:						# left inner, right outer
		rc.ForwardM1(address[RC1], inner)
		rc.ForwardM2(address[RC1], inner)
		rc.ForwardM1(address[RC2], inner)
		rc.ForwardM2(address[RC2], outer)
		rc.ForwardM1(address[RC3], outer)
		rc.ForwardM2(address[RC3], outer)
		time.sleep(int(timer))
		rc.ForwardM1(address[RC1], 0)
		rc.ForwardM2(address[RC1], 0)
		rc.ForwardM1(address[RC2], 0)
		rc.ForwardM2(address[RC2], 0)
		rc.ForwardM1(address[RC3], 0)
		rc.ForwardM2(address[RC3], 0)
		
	return 0
	
def calculate_wheel_factor():
	global FR_CENTER_RAW
	global FR_TOTAL
	global FR_FACTOR
	global FR_LEFT
	global FR_RIGHT_RAW
	
	global BR_CENTER_RAW
	global BR_TOTAL
	global BR_FACTOR
	global BR_LEFT
	global BR_RIGHT_RAW
	
	global FL_CENTER_RAW
	global FL_TOTAL
	global FL_FACTOR
	global FL_LEFT
	global FL_RIGHT_RAW
	
	global BL_CENTER_RAW
	global BL_TOTAL
	global BL_FACTOR
	global BL_LEFT
	global BL_RIGHT_RAW
	
	FR_RIGHT_RAW = (FR_TOTAL // 4) * 3
	FR_FACTOR = (FR_LEFT - FR_CENTER_RAW) // -36

	BR_RIGHT_RAW = (BR_TOTAL // 4) * 3
	BR_FACTOR = (BR_LEFT - BR_CENTER_RAW) // -36
	
	FL_RIGHT_RAW = (FL_TOTAL // 4) * 3
	FL_FACTOR = (FL_LEFT - FL_CENTER_RAW) // -36
	
	BL_RIGHT_RAW = (BL_TOTAL // 4) * 3
	BL_FACTOR = (BL_LEFT - BL_CENTER_RAW) // -36
	
	return 0
	



