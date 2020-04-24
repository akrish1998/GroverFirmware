from __future__ import print_function
import time
import math
import serial
import unittest
from roboclaw import Roboclaw
import testSuite
import commandBook

""" what user sees: prompt loop where user can send commands to move rover """
""" 
-sit in > loop until q or Q entered
-to see command list type help, or just ask me :P 
-should handle most invalid inputs nicely, but you never know what a user can to
-you can enter commands without the speed & time and the standard values are used
-all commands are NOT case sensitive
"""

def parseCommand(command, cBook):
    if(len(command) == 1):
        if(command[0] != "k" and command[0] != "kill"):
            command.append(cBook.STD_SPEED)
            command.append(cBook.STD_TIME)
    elif(len(command) == 3):
        if(command[0] == "rs"):
            command.append(cBook.STD_SPEED)
            command.append(cBook.STD_TIME)
    elif(len(command) == 4):
        command.append(cBook.STD_SPEED)
        command.append(cBook.STD_TIME)
    
    return cBook.run_command(command)

def main():
    cBook = commandBook.COMMAND_BOOK()

    command = input("> " )
    while(command != "Q" and command != "q"):
        command = command.strip()
        command = command.lower()
        if(len(command) != 0):
            command = command.split(' ')
            if(command[0] == "help"):
                cBook.print_message()
            elif(command[0] == "moreinfo"):
                cBook.printMoreInfo()
            else:
                if(parseCommand(command, cBook) == -1):
                    print("Invalid Command")
                    print("For more info, enter help")
        print("")
        command = input("> ")

    testSuite.kill_all()
    print("bye bye")
    return 0
    
if __name__ == "__main__":
	main()

