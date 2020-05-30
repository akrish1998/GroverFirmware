from __future__ import print_function
import time
import math
import serial
from roboclaw import Roboclaw
import commands

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
		print("lol gl")
		
		
	def parseCommand(self, command):
		if(command[0] == 'calibrate' and len(command)==1:
			return commands.calibrate_corner_encoders()
		
		elif(command[0]=='calibrate' and command[1]=='fr'):
			return commands.calibrate_FR()
		
		elif(command[0]=='calibrate' and command[1]=='br'):
			return commands.calibrate_BR()

		elif(command[0]=='calibrate' and command[1]=='fl'):
			return commands.calibrate_FL()
			
		elif(command[0]=='calibrate' and command[1]=='bl'):
			return commands.calibrate_BL()
			
		elif(command[0]=='turn' and command[1]=='right'):
			return commands.turn_right(command[2], command[3])
			
		elif(command[0]=='turn' and command[1]=='left'):
			return commands.turn_left(command[2], command[3])
			
		else:
			return -1
		return 0
        
