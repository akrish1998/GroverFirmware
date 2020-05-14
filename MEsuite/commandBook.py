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

SPEED_FIELD = 1
TIME_FIELD = 2
MAX_SPEED_MS = 0.1
DEFAULT_SPEED = 0.0502

class COMMAND_BOOK():
	def __init__(self):
		self.book = {}
                                                                                
		self.book["k"] = MEtests.kill_all                            
		self.book["low speed"] = MEtests.dynamicWheelTest_LowSpeed
		self.book["high speed"] = MEtests.dynamicWheelTest_HighSpeed
		self.book["dwt"] = MEtests.dynamicWheelTest


	# lists available commands so users don't have to memorize shit
	def print_message(self):
		print("")
		print("Commands: case doesn't matter")
		print("")
		print("")
		print("")
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
		
		
	def requestSpeed(self, command):
		speed = input("What speed (in m/s): ")
		speed = speed.strip()
		if len(speed) <= 0:
			print("Using default speed: 0.05 m/s")
			command.append(DEFAULT_SPEED)
			return self.requestDist(command)
			
		#try:	
		speed = speed.split(" ")
		speed = float(speed[0])
		if speed > MAX_SPEED_MS:
			print("Invalid speed")
			print("Valid speeds: 0 m/s - 0.1 m/s")
			return -1
		command.append(speed)
		return self.requestDist(command)
			
		# except:
			# print("Invalid Input")
			# return -1
			
		
	def requestDist(self, command):
		dist = input("How far (in m): ")
		dist = dist.strip()
		if len(dist) <= 0:
			print("Using default distance: 1 meter")
			command.append(1)
			return self.runCommand(command)
			
		#try:
		dist = dist.split(" ")
		dist = float(dist[0])
		command.append(dist)
		return self.runCommand(command)
		# except:
			# print("Invalid Input")
			# return -1
	
	def parseCommand(self, command):
		holder = []
		if("dynamic" in command):
			holder.append("dwt")
			return self.requestSpeed(holder)
		command = command.split(" ")
		return self.run_command(command)
		
    
        
	def run_command(self, command):        # actually calls functions after looper parses the command
		result = 0
		if(command[0] == "low"):
			result = self.book["low speed"]()
		elif(command[0] == "high"):
			result = self.book["high speed"]()
		elif(command[0] == "dwt"):
			result = self.book["dwt"](command[1], command[2])
		elif(command[0] == "k" or command[0] == "kill"):
			result = self.book["k"]()
		elif(command[0] == "help"):
			self.print_message()
		else:
			return result
        
