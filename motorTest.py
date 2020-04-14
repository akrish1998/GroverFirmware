from __future__ import print_function
import time
import serial
import math
from roboclaw import Roboclaw
import unittest



rc = Roboclaw("/dev/ttyS0",115200)
rc.Open()
#0x80 -> 128 -> roboclaw #1 wheels 4 & 5 for wheel revolution (functional)
#0x81 -> 129 -> roboclaw #2 wheels 6 & 7 for wheel revolution (functional)
#0x82 -> 130 -> roboclaw #3 wheels 8 & 9 for wheel revolution (functional)
#0x83 -> 131 -> roboclaw #4 wheels 0 & 1 for wheel rotation
#0x84 -> 132 -> roboclaw #5 wheels 2 & 3 for wheel rotation
address = [0x80,0x81,0x82,0x83,0x84]	

rc.ResetEncoders(address[0])
rc.ResetEncoders(address[1])
rc.ResetEncoders(address[2])

def ResetEncs():
	rc.ResetEncoders(address[0])
	rc.ResetEncoders(address[1])
	rc.ResetEncoders(address[2])


#Wrapper function to spin the Motors with easier interface
def spinMotor(motorID, speed):
		#serial address of roboclaw
		addr = {0: address[3],			#rc 4 corner: wheels 4 & 6 -> 3rd index -> 131 
				1: address[3],		
				2: address[4],		#rc 5 corner: wheels 7 & 9 -> 4th index -> 132
				3: address[4],	
				4: address[0],		#rc 1 drive: wheels 5 & 6 -> 0th index -> 128
				5: address[0],
				6: address[1],		#rc 2 drive: wheels 7 & 8 -> 1st index -> 129
				7: address[1],
				8: address[2],		#rc 3 drive: wheels 4 & 9 -> 2nd index -> 130
				9: address[2]}

		#drive forward
		if (speed >= 0):
			command = {0: rc.ForwardM1,
					   1: rc.ForwardM2,
					   2: rc.ForwardM1,
					   3: rc.ForwardM2,
					   4: rc.ForwardM1,
					   5: rc.BackwardM2, #backward based on wheel geometry
					   6: rc.ForwardM1,
					   7: rc.ForwardM2,
					   8: rc.BackwardM1,
					   9: rc.ForwardM2}
		else:
			command = {0: rc.BackwardM1,
					   1: rc.BackwardM2,
					   2: rc.BackwardM1,
					   3: rc.BackwardM2,
					   4: rc.BackwardM1,
					   5: rc.ForwardM2,
					   6: rc.BackwardM1,
					   7: rc.BackwardM2,
					   8: rc.ForwardM1,
					   9: rc.BackwardM2}

		speed = abs(speed)
		return command[motorID](addr[motorID],speed)

#Wrapper function to get Encoder values with easier interface
def getEnc(motorID):
	addr = {0: address[3],
			1: address[3],
			2: address[4],
			3: address[4],
			4: address[0],
			5: address[0],
			6: address[1],
			7: address[1],
			8: address[2],
			9: address[2]}
	if (motorID % 2 == 0):
		command = rc.ReadEncM1
	elif (motorID % 2 == 1):
		command = rc.ReadEncM2
	else:
		print("MotorID error")
		return
	cmd = command(addr[motorID])[1]
	if motorID == 5:
		cmd = cmd * -1
	return cmd
	
	
def getEnc2(motorID):
	if (motorID % 2 == 0):
		command = rc.ReadEncM1
	elif (motorID % 2 == 1):
		command = rc.ReadEncM2
	else:
		print("MotorID error")
		return
	cmd = command(address[motorID])[1]
	if motorID == 5:
		cmd = cmd * -1
	return cmd
	
def allForward():
	rc.ForwardM1(address[0], 100)
	rc.ForwardM2(address[0], 100)
	rc.ForwardM1(address[1], 100)
	rc.ForwardM2(address[1], 100)
	rc.ForwardM1(address[2], 100)
	rc.ForwardM2(address[2], 100)
	time.sleep(5)
	rc.ForwardM1(address[0], 0)
	rc.ForwardM2(address[0], 0)
	rc.ForwardM1(address[1], 0)
	rc.ForwardM2(address[1], 0)
	rc.ForwardM1(address[2], 0)
	rc.ForwardM2(address[2], 0)
	return 0

def allBackward():
	rc.BackwardM1(address[0], 100)
	rc.BackwardM2(address[0], 100)
	rc.BackwardM1(address[1], 100)
	rc.BackwardM2(address[1], 100)
	rc.BackwardM1(address[2], 100)
	rc.BackwardM2(address[2], 100)
	time.sleep(5)
	rc.BackwardM1(address[0], 0)
	rc.BackwardM2(address[0], 0)
	rc.BackwardM1(address[1], 0)
	rc.BackwardM2(address[1], 0)
	rc.BackwardM1(address[2], 0)
	rc.BackwardM2(address[2], 0)
	return 0


def test_motor(motorID, d):
		speed = 20
		ResetEncs()
		spinMotor(motorID,speed * d)
		time.sleep(1)
		spinMotor(motorID,0)
		return getEnc(motorID)
		
# verifies the mixed commands for individual RCs
# which determines which direction to move the wheels
def getRollin(motorID, d, which):
	speed = d * 20
		
	# tell both motors to move forward for 2 seconds then stop
	if(which == 1):
		rc.ForwardM1(address[motorID], speed)
		rc.ForwardM2(address[motorID], speed)
		time.sleep(2)
		rc.ForwardM1(address[motorID], 0)
		rc.ForwardM2(address[motorID], 0)
		
	# tell both motors to move backward for 2 seconds then stop	
	elif(which == 2):
		rc.BackwardM1(address[motorID], speed)
		rc.BackwardM2(address[motorID], speed)
		time.sleep(2)
		rc.BackwardM1(address[motorID], 0)
		rc.BackwardM2(address[motorID], 0)
		
	# spin M1 forward and M2 backward for 2 seconds then stop
	# used to determine time it takes for both wheels the move independently
	elif(which == 3):
		rc.ForwardM1(address[motorID], speed)
		rc.BackwardM2(address[motorID], speed)
		time.sleep(2)
		rc.ForwardM1(address[motorID], 0)
		rc.BackwardM2(address[motorID], 0)

	elif(which == 4):
		rc.ForwardM2(address[0], speed)
		time.sleep(2)
		rc.ForwardM2(address[0], 0)
		rc.ForwardM1(address[2], speed)
		time.sleep(2)
		rc.ForwardM1(address[2], 0)

	#Corner articulation - Forward
	# elif(which == 5):
	# 	rc.ForwardM1(address[3], speed)
	# 	time.sleep(1)
	# 	rc.ForwardM1(address[3], 0)

	# elif(which == 6):
	# 	rc.ForwardM2(address[3], speed)
	# 	time.sleep(1)
	# 	rc.ForwardM2(address[3], 0)

	# elif(which == 7):
	# 	rc.ForwardM1(address[4], speed)
	# 	time.sleep(1)
	# 	rc.ForwardM1(address[4], 0)

	# elif(which == 8):
	# 	rc.ForwardM2(address[4], speed)
	# 	time.sleep(1)
	# 	rc.ForwardM2(address[4], 0)

	#Corner articulation - Backward
	# elif(which == 9):
	# 	rc.BackwardM1(address[3], speed)
	# 	time.sleep(1)
	# 	rc.BackwardM1(address[3], 0)

	# elif(which == 10):
	# 	rc.BackwardM2(address[3], speed)
	# 	time.sleep(1)
	# 	rc.BackwardM2(address[3], 0)

	# elif(which == 11):
	# 	rc.BackwardM1(address[4], speed)
	# 	time.sleep(1)
	# 	rc.BackwardM1(address[4], 0)

	# elif(which == 12):
	# 	rc.BackwardM2(address[4], speed)
	# 	time.sleep(1)
	# 	rc.BackwardM2(address[4], 0)

		
	return getEnc2(motorID)
	

class MotorTestMethods(unittest.TestCase):


	#Testing if Absolute encoders are reading in the correct value range,
	#and quadrature encoders are reading at all
	def test_enc_sigs(self):
		for i in range(10):
			enc = getEnc(i)
			if i < 4:
				self.assertTrue(0 <= enc <= 2000)
			else:
				self.assertTrue(type(enc) is int or type(enc) is long)
	#Test each RoboClaw and make sure it's Logic and Main battery voltage
	#are within acceptable parameters
	# def test_Logic_battery0(self):
		# self.assertTrue(4.5 <= (rc.ReadLogicBatteryVoltage(address[0])[1])/10.0 <= 5.5)
	# def test_Logic_battery1(self):
		# self.assertTrue(4.5 <= (rc.ReadLogicBatteryVoltage(address[1])[1])/10.0 <= 5.5)
	# def test_Logic_battery2(self):
		# self.assertTrue(4.5 <= (rc.ReadLogicBatteryVoltage(address[2])[1])/10.0 <= 5.5)
	# def test_Logic_battery3(self):
		# self.assertTrue(4.5 <= (rc.ReadLogicBatteryVoltage(address[3])[1])/10.0 <= 5.5)	
	# def test_Logic_battery4(self):
		# self.assertTrue(4.5 <= (rc.ReadLogicBatteryVoltage(address[4])[1])/10.0 <= 5.5)

	# def test_Main_battery0(self):
		# self.assertTrue(11.5 <= (rc.ReadMainBatteryVoltage(address[0])[1])/10.0 <= 12.5)
	# def test_Main_battery1(self):
		# self.assertTrue(11.5 <= (rc.ReadMainBatteryVoltage(address[1])[1])/10.0 <= 12.5)
	# def test_Main_battery2(self):
		# self.assertTrue(11.5 <= (rc.ReadMainBatteryVoltage(address[2])[1])/10.0 <= 12.5)
	# def test_Main_battery3(self):
		# self.assertTrue(11.5 <= (rc.ReadMainBatteryVoltage(address[3])[1])/10.0 <= 12.5)
	# def test_Main_battery4(self):
		# self.assertTrue(11.5 <= (rc.ReadMainBatteryVoltage(address[4])[1])/10.0 <= 12.5)

	#Test that the encoders increase when the motors are moved forward,
	#and they decrease when motors are moved backwards
	
	# def test_motor4_F(self):
	# 	print("Motor4_F")
	# 	self.assertTrue(test_motor(4,1) > 0, msg = "Encoder Value error, should have read ABOVE 0, instead was :" + str(getEnc(4)))
	
	# def test_motor4_B(self):
	# 	print("Motor4_B")
	# 	self.assertTrue(test_motor(4,-1) < 0, msg = "Encoder Value error, should have read BELOW 0, instead was : " + str(getEnc(4))) 	

	# def test_motor5_F(self):
	# 	print("Motor5_F")
	# 	self.assertTrue(test_motor(5,1) > 0, msg = "Encoder Value error, should have read ABOVE 0, instead was : " + str(getEnc(5)))

	# def test_motor5_B(self):
	# 	print("Motor5_B")
	# 	self.assertTrue(test_motor(5,-1) < 0, msg = "Encoder Value error, should have read BELOW 0, instead was : " + str(getEnc(5)))

	# def test_motor6_F(self):
	# 	print("Motor6_F")
	# 	self.assertTrue(test_motor(6,1) > 0, msg = "Encoder Value error, should have read ABOVE 0, instead was : " + str(getEnc(6)))

	# def test_motor6_B(self):
	# 	print("Motor6_B")
	# 	self.assertTrue(test_motor(6,-1) < 0, msg = "Encoder Value error, should have read BELOW 0, instead was : " + str(getEnc(6)))

	# def test_motor7_F(self): #Motor encoder values do not invert
	# 	print("Motor7_F")
	# 	self.assertTrue(test_motor(7,1) > 0, msg = "Encoder Value error, should have read ABOVE 0, instead was : " + str(getEnc(7)))

	# def test_motor7_B(self): #Motor encoder values do not invert
	# 	print("Motor7_B")
	# 	self.assertTrue(test_motor(7,-1) < 0, msg = "Encoder Value error, should have read BELOW 0, instead was : " + str(getEnc(7)))

	# def test_motor8_F(self):
	# 	print("Motor8_F")
	# 	self.assertTrue(test_motor(8,1) > 0, msg = "Encoder Value error, should have read ABOVE 0, instead was : " + str(getEnc(8)))
	
	# def test_motor8_B(self):
	# 	print("Motor8_B")
	# 	self.assertTrue(test_motor(8,-1) < 0, msg = "Encoder Value error, should have read BELOW 0, instead was : " + str(getEnc(8)))

	# def test_motor9_F(self):
	# 	print("Motor9_F")
	# 	self.assertTrue(test_motor(9,1) > 0, msg = "Encoder Value error, should have read ABOVE 0, instead was : " + str(getEnc(9)))

	# def test_motor9_B(self):
	# 	print("Motor9_B")
	# 	self.assertTrue(test_motor(9,-1) < 0, msg = "Encoder Value error, should have read BELOW 0, instead was : " + str(getEnc(9)))
		
	
	# def test_RC1_F(self):
	# 	print("RC1_F")
	# 	self.assertTrue(getRollin(0, 1, 1) > 0, msg = "nope")
		
		
	# def test_RC1_B(self):
	# 	print("RC1_B")
	# 	self.assertTrue(getRollin(0, 1, 2) < 0, msg = "nope")
		
		
	# def test_RC1_mixed(self):
	# 	print("RC1_mixed")
	# 	self.assertTrue(getRollin(0, 1, 3) > 0, msg = "nope")
		
		
	# def test_RC2_F(self):
	# 	print("RC2_F")
	# 	self.assertTrue(getRollin(1, 1, 1) > 0, msg = "nope")
		
		
	# def test_RC2_B(self):
	# 	print("RC2_B")
	# 	self.assertTrue(getRollin(1, 1, 2) > 0, msg = "nope")
		
		
	# def test_RC2_mixed(self):
	# 	print("RC2_mixed")
	# 	self.assertTrue(getRollin(1, 1, 3) > 0, msg = "nope")
		
		
	# def test_RC3_F(self):
	# 	print("RC3_F")
	# 	self.assertTrue(getRollin(2, 1, 1) > 0, msg = "nope")
		
		
	# def test_RC3_B(self):
	# 	print("RC3_B")
	# 	self.assertTrue(getRollin(2, 1, 2) > 0, msg = "nope")
		
		
	# def test_RC3_mixed(self):
	# 	print("RC3_mixed")
	# 	self.assertTrue(getRollin(2, 1, 3) > 0, msg = "nope")

	#def test_all_F(self):
		#self.assertTrue(allForward() == 0, msg = "nope")

	#def test_all_B(self):
		#self.assertTrue(allBackward() == 0, msg = "nope")
	
	def test_RC4_F(self):
		print("RC4_F")
		self.assertTrue(getRollin(3, 1, 1) > 0, msg = "nope")

	def test_RC4_B(self):
		print("RC4_B")
		self.assertTrue(getRollin(3, 1, 2) > 0, msg = "nope")

	def test_RC5_F(self):
		print("RC5_F")
		self.assertTrue(getRollin(4, 1, 1) > 0, msg = "nope")

	def test_RC5_B(self):
		print("RC5_B")
		self.assertTrue(getRollin(4, 1, 2) > 0, msg = "nope")

	# def test_Corner1_F(self):
	# 	print("Corner 1 F")
	# 	self.assertTrue(getRollin(0, 25, 5) > 0, msg = "nope")

	# def test_Corner1_B(self):
	# 	print("Corner 1 B")
	# 	self.assertTrue(getRollin(0, 25, 9) > 0, msg = "nope")

	# def test_Corner2_F(self):
	# 	print("Corner 2 F")
	# 	self.assertTrue(getRollin(0, 25, 6) > 0, msg = "nope")

	# def test_Corner2_B(self):
	# 	print("Corner 2 B")
	# 	self.assertTrue(getRollin(0, 25, 10) > 0, msg = "nope")

	# def test_Corner3_F(self):
	# 	print("Corner 3 F")
	# 	self.assertTrue(getRollin(0, 25, 7) > 0, msg = "nope")

	# def test_Corner3_B(self):
	# 	print("Corner 3 B")
	# 	self.assertTrue(getRollin(0, 25, 11) > 0, msg = "nope")	

	# def test_Corner4_F(self):
	# 	print("Corner 4 F")
	# 	self.assertTrue(getRollin(0, 25, 8) > 0, msg = "nope")

	# def test_Corner4_B(self):
	# 	print("Corner 4 B")
	# 	self.assertTrue(getRollin(0, 25, 12) > 0, msg = "nope")


	# def test_middle(self):
	# 	self.assertTrue(getRollin(0, 1, 4) > 0, msg = "nope" )

if __name__ == '__main__':
	unittest.main()

