from __future__ import print_function
import time
import math
import unittest

#0x80 -> 128 -> roboclaw #1 wheels 4 & 5 for wheel revolution (functional)
#0x81 -> 129 -> roboclaw #2 wheels 6 & 7 for wheel revolution (functional)
#0x82 -> 130 -> roboclaw #3 wheels 8 & 9 for wheel revolution (functional)
#0x83 -> 131 -> roboclaw #4 wheels 0 & 1 for wheel rotation
#0x84 -> 132 -> roboclaw #5 wheels 2 & 3 for wheel rotation

#Takes in an array of Encoder values and the name of the test
def print_grover(encoderArray, testName):
	print("Test: ", testName)
	print("\n\t   Roboclaw 1\t\t    Roboclaw 2")
	print('\t'.ljust(17, '_'),"\t     ______")
	print("Wheel:\t4\t       5\t\t6")
	print("    --------        --------\t    --------")
	print("    |{:6}|--\t    |{:6}|\t  --|{:6}|".format(encoderArray[0],encoderArray[1],encoderArray[2]))
	print("    --------  |     --------\t |  --------")
	print("              |         |   \t |")
	print ('\t'.ljust(34, '-'))
	print("\t|\t\t\t\t|\n<--B(-)\t|\t\t\tGantry\t|  F(+)-->\n\t|\t\t\t\t|")
	print ('\t'.ljust(34, '-'))
	print("              |         |  \t |")
	print("    --------  |     --------\t |  --------")
	print("    |{:6}|--\t    |{:6}|\t  --|{:6}|".format(encoderArray[3],encoderArray[4],encoderArray[5]))
	print("    --------        --------\t    --------")
	print("Wheel:\t9\t       8\t\t7")
	print('\t'.ljust(17, '_'),"\t     ______")
	print("\t   Roboclaw 3\t\t    Roboclaw 2\n")
	print ('-'.ljust(60, '-'),"\n")

class MotorTestMethods(unittest.TestCase):
	def test_grover_print(self):
		print_grover([15337,15418,15522,15373,14901,14999], "test - Forward")
		print_grover([-15076,-15048,-12280,-15517,-15517,-15441], "test - Backward")

if __name__ == '__main__':
	unittest.main()
    
    
    
# print("Test: ", testName)
	# print("\n\t   Roboclaw 1\t\t    Roboclaw 2")
	# print('\t'.ljust(17, '_'),"\t     ______")
	# print("Wheel:\t4\t       5\t\t6")
	# print("    --------        --------\t    --------")
	# print("    |{:6}|--\t    |{:6}|\t  --|{:6}|".format(encoderArrayM1[RC1],encoderArrayM2[RC1],encoderArrayM1[RC2]))
	# print("    --------  |     --------\t |  --------")
	# print("              |         |   \t |")
	# print ('\t'.ljust(34, '-'))
	# print("\t|\t\t\t\t|\n<--B(-)\t|\t\t\tGantry\t|  F(+)-->\n\t|\t\t\t\t|")
	# print ('\t'.ljust(34, '-'))
	# print("              |         |  \t |")
	# print("    --------  |     --------\t |  --------")
	# print("    |{:6}|--\t    |{:6}|\t  --|{:6}|".format(encoderArrayM2[RC3],encoderArrayM1[RC3],encoderArrayM2[RC2]))
	# print("    --------        --------\t    --------")
	# print("Wheel:\t9\t       8\t\t7")
	# print('\t'.ljust(17, '_'),"\t     ______")
	# print("\t   Roboclaw 3\t\t    Roboclaw 2\n")
	# print ('-'.ljust(60, '-'),"\n")
