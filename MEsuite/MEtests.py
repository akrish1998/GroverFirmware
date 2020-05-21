import time
import math
import serial
import unittest
import sys
from roboclaw import Roboclaw

"""	
ME tests: functions added incrementally as MEs testing needs expanded

MEs provided with specific instruction set for their test suite

presents data that may (or may not) be useful for their needs
"""

#constants (like #define in c)
RC1 = 0
RC2 = 1
RC3 = 2
RC4 = 3
RC5 = 4

# register speeds, can be changed to whatever value you need
MIN_SPEED = 30
MAX_SPEED = 100

rc = Roboclaw("/dev/ttyS0",115200)
rc.Open()
#0x80 -> 128 -> roboclaw #1 wheels 4 & 5 for wheel spin
#0x81 -> 129 -> roboclaw #2 wheels 6 & 7 for wheel spin
#0x82 -> 130 -> roboclaw #3 wheels 8 & 9 for wheel spin
#0x83 -> 131 -> roboclaw #4 wheels 4 & 6 for wheel rotation
#0x84 -> 132 -> roboclaw #5 wheels 7 & 9 for wheel rotation
address = [0x80,0x81,0x82,0x83,0x84]	

def getRegisterSpeed(speed):
	result2 = (0.002+speed) // 0.0009
	return result2
    
    
def getTime(speed, dist):	# speed in m/s
	howLong = round((dist/speed), 1)
	return howLong
	
def getVeloInMS(speed):
	msSpeed = (0.0009 * speed) - 0.002
	return msSpeed
    
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
    

# call when running dynamic wheel tests 1, 3, 5 
# tells all wheels to turn forward relative to the front of the rover
# MIN_SPEED is 'macro' defined above as a register value, feel free to change it
# to travel 1 meter at reg speed 30 (0.025 m/s), rover rolls for roughly 40 seconds (see velocity graph)
# to invoke: low speed
def dynamicWheelTest_LowSpeed():
	print("Running forward at low speed: %s" % (((time.ctime()).split(' '))[3]))
	sys.stdout.flush()
	rc.ForwardM1(address[RC1], MIN_SPEED)
	rc.ForwardM2(address[RC1], MIN_SPEED)
	rc.ForwardM1(address[RC2], MIN_SPEED)
	rc.ForwardM2(address[RC2], MIN_SPEED)
	rc.ForwardM1(address[RC3], MIN_SPEED)
	rc.ForwardM2(address[RC3], MIN_SPEED)
	time.sleep(40)
	rc.ForwardM1(address[RC1], 0)
	rc.ForwardM2(address[RC1], 0)
	rc.ForwardM1(address[RC2], 0)
	rc.ForwardM2(address[RC2], 0)
	rc.ForwardM1(address[RC3], 0)
	rc.ForwardM2(address[RC3], 0)
	print("finished forward: %s" % (((time.ctime()).split(' '))[3]))
	sys.stdout.flush()
	
	time.sleep(5)
	print("Running backward at low speed: %s" % (((time.ctime()).split(' '))[3]))
	sys.stdout.flush()
	rc.BackwardM1(address[RC1], MIN_SPEED)
	rc.BackwardM2(address[RC1], MIN_SPEED)
	rc.BackwardM1(address[RC2], MIN_SPEED)
	rc.BackwardM2(address[RC2], MIN_SPEED)
	rc.BackwardM1(address[RC3], MIN_SPEED)
	rc.BackwardM2(address[RC3], MIN_SPEED)
	time.sleep(40)
	rc.BackwardM1(address[RC1], 0)
	rc.BackwardM2(address[RC1], 0)
	rc.BackwardM1(address[RC2], 0)
	rc.BackwardM2(address[RC2], 0)
	rc.BackwardM1(address[RC3], 0)
	rc.BackwardM2(address[RC3], 0)
	print("finished backward: %s" % (((time.ctime()).split(' '))[3]))
	sys.stdout.flush()

	return 0

# call when running dynamic wheel tests 2, 4, 6
# MAX_SPEED is 'macro' defined above as a register value, feel free to change it
# to travel 1 meter at reg speed 100 (0.085 m/s), rover rolls for roughly 11.5 seconds (see velocity graph)
# to invoke: high speed
 def dynamicWheelTest_HighSpeed():
	print("Running forward at high speed: %s" % (((time.ctime()).split(' '))[3]))
	sys.stdout.flush()
	rc.ForwardM1(address[RC1], MAX_SPEED)
	rc.ForwardM2(address[RC1], MAX_SPEED)
	rc.ForwardM1(address[RC2], MAX_SPEED)
	rc.ForwardM2(address[RC2], MAX_SPEED)
	rc.ForwardM1(address[RC3], MAX_SPEED)
	rc.ForwardM2(address[RC3], MAX_SPEED)
	time.sleep(11.5)
	rc.ForwardM1(address[RC1], 0)
	rc.ForwardM2(address[RC1], 0)
	rc.ForwardM1(address[RC2], 0)
	rc.ForwardM2(address[RC2], 0)
	rc.ForwardM1(address[RC3], 0)
	rc.ForwardM2(address[RC3], 0)
	print("finsihed forward: %s" % (((time.ctime()).split(' '))[3]))
	sys.stdout.flush()
	
	time.sleep(5)
	print("Running backward at high speed: %s" % (((time.ctime()).split(' '))[3]))
	sys.stdout.flush()
	rc.BackwardM1(address[RC1], MAX_SPEED)
	rc.BackwardM2(address[RC1], MAX_SPEED)
	rc.BackwardM1(address[RC2], MAX_SPEED)
	rc.BackwardM2(address[RC2], MAX_SPEED)
	rc.BackwardM1(address[RC3], MAX_SPEED)
	rc.BackwardM2(address[RC3], MAX_SPEED)
	time.sleep(11.5)
	rc.BackwardM1(address[RC1], 0)
	rc.BackwardM2(address[RC1], 0)
	rc.BackwardM1(address[RC2], 0)
	rc.BackwardM2(address[RC2], 0)
	rc.BackwardM1(address[RC3], 0)
	rc.BackwardM2(address[RC3], 0)
	print("finsihed backward: %s" % (((time.ctime()).split(' '))[3]))
	sys.stdout.flush()

	return 0 


def dynamicWheelTest(speed, dist):	
	print("running dynamic wheel test")
	regSpeed = getRegisterSpeed(speed);
	msSpeed = getVeloInMS(regSpeed)
	howLong = getTime(speed, dist)
	print("Running forward test at %.4f m/s" % (speed))
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
	print("Finished forward")
	
	time.sleep(5)
	print("Running backward test at %.4f m/s" % (speed))
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
	print("Finished backward")
	return 0



