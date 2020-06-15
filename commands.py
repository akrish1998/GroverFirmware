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

# corner enc values for calibration
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
CALIBRATION_SPEED = 30
SLOWER_CALIBRATION_SPEED = 25
CALIBRATION_TIME = 4
MAX_CORNER_ENC = 1550
INVALID_ENC = 1600

# arc turn constants
R_OUTER = 0.32		# 320 mm dist between corner wheels	
R_HEIGHT = 0.29		# 290 mm dist between rover center and front
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
	result2 = int(result2)
	if(result2 > 127):
		result2 = 127
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
	return enc
	
# value is the read encoder value, no wheel differientiating done here just calculations
def get_degree_by_enc(value, wheel_factor, raw_right, raw_center):
	val = int(value)
	if(value + MAX_CORNER_ENC < raw_right):
		val = val + MAX_CORNER_ENC
	
	deg = (val - raw_center) // wheel_factor
	return deg
	

# for arc turns
def get_inner_velo(degree, outer_speed):
	deg = int(degree)
	
	if(deg > MAX_TURN):
		deg = MAX_TURN
	
	outer_velo = float(outer_speed)
	percent_diff = 0.9875*(math.exp(-0.016*deg))
	inner_velo = percent_diff*outer_velo
	return inner_velo

	
def get_arc_time(degree, inner_speed):
	deg = int(degree)
	
	if(deg > MAX_TURN):
		deg = MAX_TURN
	
	rad = math.radians(deg)
	velo = float(inner_speed)
	inner_dist = R_HEIGHT/(math.tan(rad))
	arc_time = (rad*inner_dist) / velo
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

	# turn to left-most position, store left-most encoder value in global var
	rc.BackwardM1(address[RC5], CALIBRATION_SPEED)
	time.sleep(CALIBRATION_TIME)
	rc.BackwardM1(address[RC5], 0)
	left_most = rc.ReadEncM2(address[RC5])[1]
	FR_LEFT = left_most

	# turn to right-most position, adding 1550 to running total if the encoder vals wrap
	rc.ForwardM1(address[RC5], CALIBRATION_SPEED)
	start = time.time()
	while(time.time()-start<CALIBRATION_TIME):
		if(rc.ReadEncM2(address[RC5])[1] >= 1500 and flag==0):	# not using 1550 cuz the enc values change fast, so giving it wide range
			centered += MAX_CORNER_ENC
			flag = 1
	
	rc.ForwardM1(address[RC5], 0)
	right_most = rc.ReadEncM2(address[RC5])[1]	# store right-most encoder val, calculate center
	FR_RIGHT = right_most
	centered += right_most
	FR_TOTAL = centered				# see Grover Motion Derivations for info on constants
	centered = (centered+left_most)//2
	FR_CENTER_RAW = centered

	if(centered >= INVALID_ENC):
		centered -= MAX_CORNER_ENC

	# turn slower to the left so the center +/- 100 can be reached without overshooting it  
	FR_CENTER = centered
	rc.BackwardM1(address[RC5], SLOWER_CALIBRATION_SPEED)	
	while(1):
		if(centered-100 <= rc.ReadEncM2(address[RC5])[1] <= centered+100):	
			break
		time.sleep(0.25)
	rc.BackwardM1(address[RC5], 0)

	return 0


def calibrate_BR():
	print("BR")			# same idea as the FR, but with diff constants & variables
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
	rc.BackwardM2(address[RC5], SLOWER_CALIBRATION_SPEED)
	while(1):
		if(centered-100 <= rc.ReadEncM1(address[RC5])[1] <= centered+100):
			break
		time.sleep(0.25)
	rc.BackwardM2(address[RC5], 0)

	return 0
	
	
def calibrate_BL():
	print("BL")		# same idea as the FR, but with diff constants & variables
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
	rc.BackwardM1(address[RC4], SLOWER_CALIBRATION_SPEED)
	while(1):
		if(centered-100 <= rc.ReadEncM2(address[RC4])[1] <= centered+100):
			break
		time.sleep(0.25)
	rc.BackwardM1(address[RC4], 0)

	return 0
	
	
def calibrate_FL():
	print("FL")		# same idea as the FR, but with diff constants & variables
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
	rc.BackwardM2(address[RC4], SLOWER_CALIBRATION_SPEED)
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
	calibrate_BR()
	calibrate_BL()
	calibrate_FL()
	calculate_wheel_factor()
	return 0
	
	
# tells all motors to stop, direction does not matter since 0 is default stop
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
	

# calculates wheel's current position, whether to turn left or right, then turns to their centers
def recenter_wheels_prototype():
	done = 0
	fl_done = 0
	bl_done = 0
	fr_done = 0
	br_done = 0
	
	read_fl = rc.ReadEncM1
	read_bl = rc.ReadEncM2
	read_fr = rc.ReadEncM2
	read_br = rc.ReadEncM1

	current_fl = read_fl(address[RC4])[1]
	current_bl = read_bl(address[RC4])[1]
	current_fr = read_fr(address[RC5])[1]
	current_br = read_br(address[RC5])[1]
	
	if(current_fl + MAX_CORNER_ENC > FL_RIGHT_RAW):		
		fl = rc.ForwardM2
	else:										
		fl = rc.BackwardM2
		
		
	if(current_bl + MAX_CORNER_ENC > BL_RIGHT_RAW):		
		bl = rc.ForwardM1
	else:										
		bl = rc.BackwardM1
		
		
	if(current_fr + MAX_CORNER_ENC > FR_RIGHT_RAW):		
		fr = rc.ForwardM1
	else:										
		fr = rc.BackwardM1
		
		
	if(current_br + MAX_CORNER_ENC > FL_RIGHT_RAW):		
		br = rc.ForwardM2
	else:										
		br = rc.BackwardM2
		
		
	fl(address[RC4], SLOWER_CALIBRATION_SPEED)
	bl(address[RC4], SLOWER_CALIBRATION_SPEED)
	fr(address[RC5], SLOWER_CALIBRATION_SPEED)
	br(address[RC5], SLOWER_CALIBRATION_SPEED)
		
	while(done < 4):
		if(FL_CENTER-100 <= read_fl(address[RC4])[1] <= FL_CENTER + 100 and fl_done == 0):
			fl(address[RC4], 0)
			done = done + 1
			fl_done = 1
			
		if(BL_CENTER-100 <= read_bl(address[RC4])[1] <= BL_CENTER + 100 and bl_done == 0):
			bl(address[RC4], 0)
			done = done + 1
			bl_done = 1
		
		if(FR_CENTER-100 <= read_fr(address[RC5])[1] <= FR_CENTER + 100 and fr_done == 0):
			fr(address[RC5], 0)
			done = done + 1
			fr_done = 1
			
		if(BR_CENTER-100 <= read_br(address[RC5])[1] <= BR_CENTER + 100 and br_done == 0):
			br(address[RC5], 0)
			done = done + 1
			br_done = 1
			
	fl(address[RC4], 0)		# just in case ....
	bl(address[RC4], 0)
	fr(address[RC5], 0)
	br(address[RC5], 0)
		
	return 0
	

# less reliant on encoders read
# turns all wheels to left-most turn position, then turns to right until centers reached
def recenter_wheels():
	done = 0
	fl_done = 0
	bl_done = 0
	fr_done = 0
	br_done = 0
	
	rc.BackwardM1(address[RC4], CALIBRATION_SPEED)	# BL
	rc.BackwardM2(address[RC4], CALIBRATION_SPEED)	# FL
	rc.BackwardM1(address[RC5], CALIBRATION_SPEED)	# FR
	rc.BackwardM2(address[RC5], CALIBRATION_SPEED)	# BR
	time.sleep(3)
	rc.BackwardM1(address[RC4], 0)
	rc.BackwardM1(address[RC4], 0)
	rc.BackwardM1(address[RC5], 0)
	rc.BackwardM1(address[RC5], 0)
	
	read_fl = rc.ReadEncM1
	read_bl = rc.ReadEncM2
	read_fr = rc.ReadEncM2
	read_br = rc.ReadEncM1
	
	rc.ForwardM1(address[RC4], SLOWER_CALIBRATION_SPEED)	# BL
	rc.ForwardM2(address[RC4], SLOWER_CALIBRATION_SPEED)	# FL
	rc.ForwardM1(address[RC5], SLOWER_CALIBRATION_SPEED)	# FR
	rc.ForwardM2(address[RC5], SLOWER_CALIBRATION_SPEED)	# BR
	
	while(done < 4):
		if((FL_CENTER-100 <= read_fl(address[RC4])[1] <= FL_CENTER + 100) and fl_done == 0):
			rc.ForwardM2(address[RC4], 0)
			done = done + 1
			fl_done = 1
			
		if((BL_CENTER-100 <= read_bl(address[RC4])[1] <= BL_CENTER + 100) and bl_done == 0):
			rc.ForwardM1(address[RC4], 0)
			done = done + 1
			bl_done = 1
		
		if((FR_CENTER-100 <= read_fr(address[RC5])[1] <= FR_CENTER + 100) and fr_done == 0):
			rc.ForwardM2(address[RC5], 0)
			done = done + 1
			fr_done = 1
			
		if((BR_CENTER-100 <= read_br(address[RC5])[1] <= BR_CENTER + 100) and br_done == 0):
			rc.BackwardM2(address[RC5], 0)
			done = done + 1
			br_done = 1
			
			
	fl(address[RC4], 0)		# just in case ....
	bl(address[RC4], 0)
	fr(address[RC5], 0)
	br(address[RC5], 0)
		
	return 0	
		

# see documentation on articulation calculations for description & derivation		
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


# drives rover straight forward at specified speed for specified distance	
def forward(speed, dist):

	if(dist <= 0):
		print("Invalid distance entered: %.2f", % (dist))
		return -1

	regSpeed = get_register_speed(speed);
	regSpeed = int(regSpeed)
	howLong = get_time(speed, dist)

	print("Driving forward at %.4f m/s for %.2f meters" % (speed, howLong))

	rc.ForwardM1(address[RC1], regSpeed)
	rc.ForwardM2(address[RC1], regSpeed)
	rc.ForwardM1(address[RC2], regSpeed)
	rc.ForwardM2(address[RC2], regSpeed)
	rc.ForwardM1(address[RC3], regSpeed)
	rc.ForwardM2(address[RC3], regSpeed)
	time.sleep(howLong)
	rc.ForwardM1(address[RC1], 0)
	rc.ForwardM2(address[RC1], 0)
	rc.ForwardM1(address[RC2], 0)
	rc.ForwardM2(address[RC2], 0)
	rc.ForwardM1(address[RC3], 0)
	rc.ForwardM2(address[RC3], 0)
	return 0
	

# drives rover straight backward at specified speed for specified distance
def backward(speed, dist):
	if(dist <= 0):
		print("Invalid distance entered: %.2f", % (dist))
		return -1

	regSpeed = get_register_speed(speed);
	regSpeed = int(regSpeed)
	howLong = get_time(speed, dist)

	print("Driving backward at %.4f m/s for %.2f meters" % (speed, howLong))

	rc.BackwardM1(address[RC1], regSpeed)
	rc.BackwardM2(address[RC1], regSpeed)
	rc.BackwardM1(address[RC2], regSpeed)
	rc.BackwardM2(address[RC2], regSpeed)
	rc.BackwardM1(address[RC3], regSpeed)
	rc.BackwardM2(address[RC3], regSpeed)
	time.sleep(howLong)
	rc.BackwardM1(address[RC1], 0)
	rc.BackwardM2(address[RC1], 0)
	rc.BackwardM1(address[RC2], 0)
	rc.BackwardM2(address[RC2], 0)
	rc.BackwardM1(address[RC3], 0)
	rc.BackwardM2(address[RC3], 0)
	return 0
	

# rotates corner wheels to guessed positions for an arc turn
# inner wheel rotation > outer wheel rotation
#	- inner wheels rotated to their fully turned position (36)
#	- outer wheels rotated slightly less than the inner wheels
#	  done by reducing wheel rotation speed
#	(what that angle and speed is, we don't know :P)
def generic_turn(direction):
	if(direction == 'right'):				# right turn, left wheels outer, right inner
		rc.ForwardM2(address[RC4], 9)			# FL
		rc.ForwardM1(address[RC5], CALIBRATION_SPEED)	# FR
		rc.BackwardM1(address[RC4], 9)			# BL
		rc.BackwardM2(address[RC5], 23)			# BR this one rotates beyond its stopper which we want to avoid
	else:							# left turn, right wheels outer
		rc.BackwardM2(address[RC4], CALIBRATION_SPEED)	# FL
		rc.BackwardM1(address[RC5], 10)			# FR
		rc.ForwardM1(address[RC4], CALIBRATION_SPEED)	# BL
		rc.ForwardM2(address[RC5], 8)			# BR

	time.sleep(3)
	rc.BackwardM2(address[RC4], 0)
	rc.BackwardM1(address[RC5], 0)
	rc.BackwardM1(address[RC4], 0)
	rc.BackwardM2(address[RC5], 0)

	return 0


# turns wheels according to turning direction using generic function (not user specified)
# directs command to arc turn speeds and which direction (drive direction, forward/backward)
def turn(speed, direction, dist, drive):	
	generic_turn(direction)
	distance = float(dist)

	if(dist==0):
		if(drive=='forward'):
			return arc_turn_forward(direction, speed)
		else:
			return arc_turn_backward(direction, speed)
	else:
		if(drive=='forward'):
			return arc_turn_forward_dist(direction, speed, distance)
		else:
			return arc_turn_backward_dist(direction, speed, distance)
	return 0

# drives rover forward for arc turns at specified speed until user tells it to stop
# at some point can have a specified distance to turn until, so time limit used from there 
def arc_turn_forward(direction, speed):
	outer_speed = float(speed)
	outer = get_register_speed(outer_speed)
	inner_speed = get_inner_velo(MAX_TURN, outer_speed)
	inner = get_register_speed(inner_speed)
	
	if(direction=='right'):				# right turn: right inner, left outer
		rc.ForwardM1(address[RC1], outer)
		rc.ForwardM2(address[RC1], outer)
		rc.ForwardM1(address[RC2], outer)
		rc.ForwardM2(address[RC2], inner)
		rc.ForwardM1(address[RC3], inner)
		rc.ForwardM2(address[RC3], inner)
	else:						# left turn: left inner, right outer
		rc.ForwardM1(address[RC1], inner)
		rc.ForwardM2(address[RC1], inner)
		rc.ForwardM1(address[RC2], inner)
		rc.ForwardM2(address[RC2], outer)
		rc.ForwardM1(address[RC3], outer)
		rc.ForwardM2(address[RC3], outer)
	
	stopper = raw_input("stop?  ")
	while(stopper != "y" and stopper != "yes"):
		stopper = raw_input("stop? (y/n):  ")
	
	rc.ForwardM1(address[RC1], 0)
	rc.ForwardM2(address[RC1], 0)
	rc.ForwardM1(address[RC2], 0)
	rc.ForwardM2(address[RC2], 0)
	rc.ForwardM1(address[RC3], 0)
	rc.ForwardM2(address[RC3], 0)

	return 0
	
# same as above but backwards
def arc_turn_backward(direction, speed):
	outer_speed = float(speed)
	outer = get_register_speed(outer_speed)
	inner_speed = get_inner_velo(MAX_TURN, outer_speed)
	inner = get_register_speed(inner_speed)
	
	if(direction=='right'):				# right turn: right inner, left outer
		rc.BackwardM1(address[RC1], outer)
		rc.BackwardM2(address[RC1], outer)
		rc.BackwardM1(address[RC2], outer)
		rc.BackwardM2(address[RC2], inner)
		rc.BackwardM1(address[RC3], inner)
		rc.BackwardM2(address[RC3], inner)
	else:						# left turn: left inner, right outer
		rc.BackwardM1(address[RC1], inner)
		rc.BackwardM2(address[RC1], inner)
		rc.BackwardM1(address[RC2], inner)
		rc.BackwardM2(address[RC2], outer)
		rc.BackwardM1(address[RC3], outer)
		rc.BackwardM2(address[RC3], outer)
	
	stopper = raw_input("stop?  ")
	while(stopper != "y" and stopper != "yes"):
		stopper = raw_input("stop?  ")
	
	rc.BackwardM1(address[RC1], 0)
	rc.BackwardM2(address[RC1], 0)
	rc.BackwardM1(address[RC2], 0)
	rc.BackwardM2(address[RC2], 0)
	rc.BackwardM1(address[RC3], 0)
	rc.BackwardM2(address[RC3], 0)

	return 0
	

# drives rover forward for arc turn at specified speed for specified distance
def arc_turn_forward_dist(direction, speed, dist):
	outer_speed = float(speed)
	outer = get_register_speed(outer_speed)
	inner_speed = get_inner_velo(MAX_TURN, outer_speed)
	inner = get_register_speed(inner_speed)
	timer = get_time(speed, dist)
	
	if(direction=='right'):				# right turn: right inner, left outer
		rc.ForwardM1(address[RC1], outer)
		rc.ForwardM2(address[RC1], outer)
		rc.ForwardM1(address[RC2], outer)
		rc.ForwardM2(address[RC2], inner)
		rc.ForwardM1(address[RC3], inner)
		rc.ForwardM2(address[RC3], inner)
	else:						# left turn: left inner, right outer
		rc.ForwardM1(address[RC1], inner)
		rc.ForwardM2(address[RC1], inner)
		rc.ForwardM1(address[RC2], inner)
		rc.ForwardM2(address[RC2], outer)
		rc.ForwardM1(address[RC3], outer)
		rc.ForwardM2(address[RC3], outer)

	time.sleep(timer)
	
	rc.BackwardM1(address[RC1], 0)
	rc.BackwardM2(address[RC1], 0)
	rc.BackwardM1(address[RC2], 0)
	rc.BackwardM2(address[RC2], 0)
	rc.BackwardM1(address[RC3], 0)
	rc.BackwardM2(address[RC3], 0)
	
	return 0


# drives rover backward for arc turn at specified speed for specified distance
def arc_turn_backward_dist(direction, speed, dist):
	outer_speed = float(speed)
	outer = get_register_speed(outer_speed)
	inner_speed = get_inner_velo(MAX_TURN, outer_speed)
	inner = get_register_speed(inner_speed)
	timer = get_time(speed, dist)
	
	if(direction=='right'):				# right turn: right inner, left outer
		rc.BackwardM1(address[RC1], outer)
		rc.BackwardM2(address[RC1], outer)
		rc.BackwardM1(address[RC2], outer)
		rc.BackwardM2(address[RC2], inner)
		rc.BackwardM1(address[RC3], inner)
		rc.BackwardM2(address[RC3], inner)
	else:						# left turn: left inner, right outer
		rc.BackwardM1(address[RC1], inner)
		rc.BackwardM2(address[RC1], inner)
		rc.BackwardM1(address[RC2], inner)
		rc.BackwardM2(address[RC2], outer)
		rc.BackwardM1(address[RC3], outer)
		rc.BackwardM2(address[RC3], outer)
		
	time.sleep(timer)
	
	rc.BackwardM1(address[RC1], 0)
	rc.BackwardM2(address[RC1], 0)
	rc.BackwardM1(address[RC2], 0)
	rc.BackwardM2(address[RC2], 0)
	rc.BackwardM1(address[RC3], 0)
	rc.BackwardM2(address[RC3], 0)
	
	return 0
	
	
	
	
# prototype of how articulation could be done when any angle between -36/+36 from any current position
# not tested too much, def not reliable, but general algorithm is effective
# see documentation for how these equations were derived
def articulate_FR(direction, speed, degree):
	
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




