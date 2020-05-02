import time
import math
import serial
from roboclaw import Roboclaw
import MEtests

""" 
maps user entered commands to their corresponding functions 

if user enters invalid command (doesn't exist, incorrect spelling, invalid parameter, etc)
error message printed

"""

class COMMAND_BOOK():
	def __init__(self):
		self.book = {}
                                                                                
		self.book["k"] = MEtests.kill_all                            
		self.book["low speed"] = MEtests.dynamicWheelTest_LowSpeed
		self.book["high speed"] = MEtests.dynamicWheelTest_HighSpeed


	# lists available commands so users don't have to memorize shit
	def print_message(self):
		print("")
		print("Commands: case doesn't matter")
		print("")
		print("low speed")
		print("runs the dynamic wheel test at low speed (tests 1, 3, 5)")
		print("")
		print("high speed")
		print("runs the dynamic wheel test at high speed (tests 2, 4, 6)")
		print("")
		print("k or kill")
		print("kill switch: tells all motors to stop moving in the case of an emergency")
		print("")
    
        
	def run_command(self, command):        # actually calls functions after looper parses the command
		result = 0
		if(command[0] == "low"):
			result = self.book["low speed"]()
		elif(command[0] == "high"):
			result = self.book["high speed"]()
		elif(command[0] == "k" or command[0] == "kill"):
			result = self.book["k"]()
		elif(command[0] == "help"):
			self.print_message()
		else:
			return result
        
