from __future__ import print_function
import time
import math
import serial
import unittest
from roboclaw import Roboclaw
import commands
import commandBook

""" what user sees: prompt loop where user can send commands to move rover """
""" 
-sit in > loop until q or Q entered
-to see command list type help, or just ask me :P 
-should handle most invalid inputs nicely, but you never know what a user can to
-you can enter commands without the speed & time and the standard values are used
-all commands are NOT case sensitive
"""

def main():
	cBook = commandBook.COMMAND_BOOK()

	command = raw_input("> " )
	while(command != "Q" and command != "q"):
		command = command.strip()
		command = command.lower()
		if(len(command) != 0):
			command = command.split(' ')
			if(command[0] == "help"):
				cBook.print_message()
			else:
				if(cBook.parseCommand(command) == -1):
					print("For more info, enter help")
		print("")
		command = raw_input("> ")

	commands.kill_all()
	print("bye bye")
	return 0
    
if __name__ == "__main__":
	main()

