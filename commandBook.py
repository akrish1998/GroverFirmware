from __future__ import print_function
import time
import math
import serial
from roboclaw import Roboclaw
import testSuite

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
		self.STD_SPEED = 60             # standard constants that are used when no spped or time specified
		self.STD_TIME = 5
                                                                                # total command length
		self.book["raf"] = testSuite.roll_all_forward                  # 1 - 3 args
		self.book["rab"] = testSuite.roll_all_backward                 # 1 - 3 args
		self.book["aar"] = testSuite.articulate_all_corners_right      # 1 - 3 args
		self.book["aal"] = testSuite.articulate_all_corners_left       # 1 - 3 args
		self.book["rs"] = testSuite.rotate_set                         # 3 - 5 args
		self.book["ri"] = testSuite.rotate_individual_wheel            # 4 - 6 args
		self.book["k"] = testSuite.kill_all                            # 1 args
		self.book["kill"] = testSuite.kill_all                         # 1 args


    # dumps this info when user enters help cuz I'm dumb and can't remember every command and its field
	def print_message(self):
		print("")
		print("Commands: case doesn't matter")
		print("Fields:")
		print("[] required field    <> optional field")
		print("? integer user input")
		print("DO NOT include [] <> ?  ->  ex: ASF 40 4")
		print("")
		print("[K]<ill>")
		print("stops all motors")
		print("")
		print("[RAF] <speed?> <time?>")
		print("all wheels spin forward")
		print("")
		print("[RAB] <speed?> <time?>")
		print("all wheels spin backward at <speed?> for <time?> seconds")
		print("")
		print("[RS] [rc?] [test?] <speed?> <time?>")
		print("wheel set [rc?] runs [test?] at <speed?> for <time?> seconds")
		print("")
		print("[RI] [rc?] [wheel?] [direction?] <speed?> <time?>")
		print("rotates [wheel?] from set [rc?] in [direction?] at <speed?> for <time?> seconds")
		print("")
		print("[AAR] <speed?> <time?>")
		print("turns all wheel to the right at <speed?> for <time?> seconds")
		print("")
		print("[AAL] <speed?> <timer?>")
		print("turns all wheels to the left at <speed?> for <time?> seconds")
		print("")
		print("q or Q to quit")
		print("")
        
	def printMoreInfo(self):        # TBD
		print("idk yet lol")
    
        
	def run_command(self, command):        # actually calls functions after looper parses the command
		result = 0
		try:
			if(len(command) == 1):
				result = self.book[command[0]]()
			elif(len(command) == 3):
				result = self.book[command[0]](command[1], command[2])
			elif(len(command) == 4):
				result = self.book[command[0]](command[1], command[2], command[3])
			elif(len(command) == 5):
				result = self.book[command[0]](command[1], command[2], command[3], command[4])
			elif(len(command) == 6):
				result = self.book[command[0]](command[1], command[2], command[3], command[4], command[5])
			else:
				return -1
			return result

		except:
			testSuite.kill_all()                            # safe exit if command fails & rover still moving
			return -1
        
