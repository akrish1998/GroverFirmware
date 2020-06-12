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
		print("[] -> required parameter")
		print("<> -> optional parameter")
		print("do NOT include [] & <> in actual command")
		print("")
		print("calibrate")
		print("calibrates all wheels")
		print("")
		print("calibrate fr")
		print("calibrates front right wheel")
		print("calibrate br")
		print("calibrates back right wheel")
		print("calibrate fl")
		print("calibrates front left wheel")
		print("calibrate bl")
		print("calibrates back left wheel")
		print("")
		print("forward [speed] [distance]")
		print("drives rover straight forward")
		print("speed: 0 - 0.1 m/s")
		print("distance: any value above 0 in m")
		print("")
		print("backward [speed] [distance]")
		print("drives rover straight backward")
		print("speed: 0 - 0.1 m/s")
		print("distance: any value above 0 in m")
		print("")
		print("arc turn [drive direction] [turn direction] [speed] <distance>")
		print("drive direction: forward or backward")
		print("turn direction: right or left")
		print("speed: 0 - 0.1 m/s")
		print("optional distance: any value above 0 in m")
		print("")
		print("recenter")
		print("recenters corner wheels")
		print("NOT FUNCTIONAL USE AT YOUR OWN RISK")
		print("")
		print("For even more info see DESCRIPTIONS file")
		print("")
		
		
		
		
	def parseCommand(self, command):
		#try:
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

		elif(command[0] == 'arc' and len(command)==5):
			return commands.turn(command[4], command[3], 0, command[2])
			
		elif(command[0]=='arc' and len(command)==6):
			return commands.turn(command[4], command[3], command[5], command[2])
			
		elif(command[0]=='recenter' and len(command)==1):
			return commands.recenter_wheels()		# turns all wheels fully left, then to center
			
		elif(command[0]=='recenter'):				# rotates from current wheel position to center
			return commands.recenter_wheels_prototype()
			
		elif(command[0]=='forward'):
			return commands.forward(command[1], command[2])
			
		elif(command[0]=='backward'):
			return commands.backward(ommand[1], command[2])
		
		else:
			return -1
		return 0
		# except:
			# commands.kill_all()
			# return -1
