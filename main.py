import serial
import os
from time import sleep
from datetime import datetime
import time
import sys


import time
import serial
import math
from roboclaw import Roboclaw
import unittest



rc = Roboclaw("/dev/ttyS0",115200)
rc.Open()
address = [0x80,0x81,0x82,0x83,0x84]



xbee_radio = serial.Serial(port='/dev/ttyUSB0',baudrate=115200)    # Radio

xbee_radio.close()

xbee_radio.open()








try:
    while True:
        line = ' '
        if xbee_radio.in_waiting:
            line = str(xbee_radio.readline())[0]
            print('------------Input--------')
            print(line)# Connected to Radio
            print(line[0] == 'w')
            print('------------Input--------')
        #motor_drive(line)
        
        if line == 'w':
            rc.ForwardM1(128, 20)
            rc.ForwardM2(128, 20)
            rc.BackwardM1(129, 20)
            rc.ForwardM2(129, 20)
            rc.ForwardM1(130, 20)
            rc.ForwardM2(130, 20)
            time.sleep(2)
            rc.ForwardM1(128, 20)
            rc.ForwardM2(128, 20)
            rc.BackwardM1(129, 20)
            rc.ForwardM2(129, 20)
            rc.ForwardM1(130, 20)
            rc.ForwardM2(130, 20)
            print('mooooooove')

        elif line == 'a':
            rc.ForwardM1(131, 40)
            time.sleep(1)
            rc.BackwardM1(131, 40)
            rc.BackwardM1(131, 0)
            
            rc.ForwardM2(131, 40)
            time.sleep(1)
            rc.BackwardM2(131, 40)
            rc.BackwardM2(131, 0) 
            
            rc.ForwardM1(132, 40)
            time.sleep(1)
            rc.BackwardM1(132, 40)
            rc.BackwardM1(132, 0)
            
            rc.ForwardM2(132, 40)
            time.sleep(1)
            rc.BackwardM2(132, 40)
            rc.BackwardM2(132, 0)          
            

        elif line == 's':
            rc.BackwardM1(128, 20)
            rc.BackwardM2(128, 20)
            rc.ForwardM1(129, 20)
            rc.BackwardM2(129, 20)
            rc.BackwardM1(130, 20)
            rc.BackwardM2(130, 20)

        elif line == 'd':
            rc.BackwardM1(128, 20)
            rc.BackwardM2(128, 20)
            rc.BackwardM1(129, 20)
            rc.ForwardM2(129, 20)
            rc.ForwardM1(130, 20)
            rc.ForwardM2(130, 20)

        elif line == 'k':
            rc.ForwardM1(128, 0)
            rc.ForwardM2(128, 0)
            rc.ForwardM1(129, 0)
            rc.ForwardM2(129, 0)
            rc.ForwardM1(130, 0)
            rc.ForwardM2(130, 0)
            rc.ForwardM1(131, 0)
            rc.ForwardM2(131, 0)
            rc.ForwardM1(132, 0)
            rc.ForwardM2(132, 0)
    
        xbee_radio.write('Command:')
        xbee_radio.write(line)
        xbee_radio.write("\r\n") 
        

except:
    xbee_radio.write("***** ERROR *****")
    xbee_radio.write("\r\n")







