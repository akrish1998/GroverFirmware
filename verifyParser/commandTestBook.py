from __future__ import print_function
import time
import math
#import serial
#from roboclaw import Roboclaw
import stupidFuncs
#import testSuite

class COMMAND_BOOK():
	def __init__(self):
		self.book = {}
		self.STD_SPEED = 60
		self.STD_TIME = 5
											# total command length
		self.book["raf"] = stupidFuncs.roll_all_forward                  # 1 - 3 args
		self.book["rab"] = stupidFuncs.roll_all_backward                 # 1 - 3 args
		self.book["aar"] = stupidFuncs.articulate_all_corners_right      # 1 - 3 args
		self.book["aal"] = stupidFuncs.articulate_all_corners_left       # 1 - 3 args
		self.book["rs"] = stupidFuncs.rotate_set                         # 3 - 5 args
		self.book["ri"] = stupidFuncs.rotate_individual_wheel            # 4 - 6 args
		self.book["k"] = stupidFuncs.kill_all                            # 1 args
		self.book["kill"] = stupidFuncs.kill_all                         # 1 args
        
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
        
	def printMoreInfo(self):
		print("idk yet lol")
    
        
	def run_command(self, command):         # actually calls functions
		result = 0
		#try:
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
            
        # except:
            # stupidFuncs.kill_all()          # safe exit if command fails & rover still moving
            # return -1 
        