from __future__ import print_function
import time
import math
import serial
from roboclaw import Roboclaw
import commands

MAX_TURN = 36

""" 'manual' for avail commands / command cookbook """
""" 
to add new func / command: 
    - add its acroynm to the dictonary with it's corresponding function to the book dictionary
        > don't include the () since that's the dereference to call the function
    - adjust run_command and parseCommand from looper is necessary
"""

class COMMAND_BOOK():
	def __init__(self):
		self.book = {}


    # dumps this info when user enters help cuz I'm dumb and can't remember every command and its field
	def print_message(self):
		print("Available commands")
		print("[] field specifies a required parameter to enter")
		print("<> field specifies an optional parameter to enter")
		print("")
		print("calibrate <flag>")
		print("calibrates all wheels when no flag specified")
		print("flags: can only call one at a time")
		print("fr -> front right")
		print("br -> back right")
		print("fl -> front left")
		print("bl -> back left")
		print("")
		print("arc turn [drive direction] [turn direction] [speed]")
		print("drive direction: forward or backward")
		print("turn direction: right or left")
		print("speed: 0 - 0.1 m/s")
		print("")
		print("recenter")
		print("recenters corner wheels")
		print("")
		
		
		
		
	def parseCommand(self, command):
		if(command[0] == 'calibrate' and len(command)==1):
			return commands.calibrate_corner_encoders()
		
		elif(command[0]=='calibrate' and command[1]=='fr'):
			return commands.calibrate_FR()
		
		elif(command[0]=='calibrate' and command[1]=='br'):
			return commands.calibrate_BR()

		elif(command[0]=='calibrate' and command[1]=='fl'):
			return commands.calibrate_FL()
			
		elif(command[0]=='calibrate' and command[1]=='bl'):
			return commands.calibrate_BL()

		elif(command[0] == 'arc'):
			return commands.turn(command[4], command[3], 0, command[2])
			
		elif(command[0]=='recenter' and len(command)==1):
			return commands.recenter_wheels()		# turns all wheels fully left, then to center
			
		elif(command[0]=='recenter'):				# rotates from current wheel position to center
			return commands.recenter_wheels_prototype()
		
		else:
			return -1
		return 0
        
