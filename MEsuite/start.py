import time
import math
import serial
import unittest
from roboclaw import Roboclaw
import MEtests
import commandBook

""" 
what user sees: sit in loop until user quits/exits or system dies

tried to make it a little more user friendly, but I'm not the user so...
"""

def main():
	cBook = commandBook.COMMAND_BOOK()

	command = raw_input("Enter Command: " )
	while(command != "Q" and command != "q"):
		command = command.strip()
		command = command.lower()
		if(len(command) != 0):
			#command = command.split(' ')
			#if(cBook.run_command(command) == -1):
			if(cBook.parseCommand(command) == -1):
				print("Invalid Command")
				print("For more info, enter help")
		print("")
		command = raw_input("Enter Command: ")

	MEtests.kill_all()
	print("bye bye")
	return 0
    
if __name__ == "__main__":
	main()

