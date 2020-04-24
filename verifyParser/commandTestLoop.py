from __future__ import print_function
import time
import math
#import serial
#from roboclaw import Roboclaw
import stupidFuncs
import commandTestBook

""" 
verifies parsing functionality in prompt loop and the command booklet 
will indicate errors on invalid input or if reads from the booklet fail
all commands are NOT case sensitive
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
    cBook = commandTestBook.COMMAND_BOOK()                          # create booklet

    command = input("> " )                                      
    while(command != "Q" and command != "q"):  
        command = command.strip()                               # sit in prompt loop until user quits or program crashes
        command = command.lower()                               # convert input to all lowercase
        if(len(command) != 0):
            command = command.split(' ')                        # split command based on spaces
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

    stupidFuncs.kill_all()                               # kill all issued to ensure rover isn't stuck moving when program exits
    print("bye bye")
    return 0
    
if __name__ == "__main__":
	main()

