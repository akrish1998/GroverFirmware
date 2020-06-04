from __future__ import print_function
import time
import math
import socket
import os
import serial
import unittest
from roboclaw import Roboclaw
from bluetooth import *

RC1 = 0
RC2 = 1
RC3 = 2
RC4 = 3
RC5 = 4

bt_sock = None

address = [0x80, 0x81, 0x82, 0x83, 0x84]

rc = Roboclaw("/dev/ttyS0", 115200)
rc.Open()

def main():

        global bt_sock

	bluetoothConnection()

	#READING COMMANDS
	while 1:
		print("reading from bluetooth Socket")
		time.sleep(0.1)
		try:
			print("sockData")
			sockData = bt_sock.recv(1024)
			print("Sock data received")
			bt_sock.send('1')
			print("sent receive")
			velocity = ord(sockData[3]) - 100
			print("velocity: ")
			print(velocity)
		
			if (velocity < 0):
				print("Moving backwards!")
				moveBackward(abs(velocity))
				print("Finished moving backwards")
			elif (velocity > 0):
				print("Moving forwards!")
				moveForward(abs(velocity))
				print("Finished moving forward")
			else:
				print("Stopping!")
				stopAll()
				print("Stoppped")
		except:
			print("Unable to process data from App! Stopping!")
			stopAll()
			bluetoothConnection()
			pass

	#CLOSING CONNECTION
	try:
		bt_sock.send('0')
		time.sleep(0.25)
		bt_sock.close()
	except:

		print("Unable to successfully close socket!")
		pass

def bluetoothConnection():
        
        print("Setting up bluetooth connection")

	global bt_sock

	#BLUETOOTH SETUP
	bt_sock = None

	server_sock = BluetoothSocket(RFCOMM)
	server_sock.bind(("", PORT_ANY))
	server_sock.listen(1)

	port = server_sock.getsockname()[1]

	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	name = "groverRover"

	advertise_service( server_sock, name,
					   service_id = uuid,
					   service_classes = [uuid, SERIAL_PORT_CLASS],
					   profiles = [SERIAL_PORT_PROFILE],
					   )
	
	print("waiting for connection on RFCOMM channel")
	print(port)
	
	client_socket, client_info = server_sock.accept()
	client_socket.setblocking(0)
	
	print("Accepted connection")
	print(client_info)

	bt_sock = client_socket
	bt_sock.settimeout(1)

def moveForward(speed):
	rc.ForwardM1(address[RC1], speed)
	rc.ForwardM2(address[RC1], speed)
	rc.ForwardM1(address[RC2], speed)
	rc.ForwardM2(address[RC2], speed)
	rc.ForwardM1(address[RC3], speed)
	rc.ForwardM2(address[RC3], speed)
	return 0

def moveBackward(speed):
	rc.BackwardM1(address[RC1], speed)
	rc.BackwardM2(address[RC1], speed)
	rc.BackwardM1(address[RC2], speed)
	rc.BackwardM2(address[RC2], speed)
	rc.BackwardM1(address[RC3], speed)
	rc.BackwardM2(address[RC3], speed)
	return 0

def stopAll():

	rc.ForwardM1(address[RC1], 0)
	rc.ForwardM2(address[RC1], 0)
	rc.ForwardM1(address[RC2], 0)
	rc.ForwardM2(address[RC2], 0)
	rc.ForwardM1(address[RC3], 0)
	rc.ForwardM2(address[RC3], 0)

	return 0

if __name__ == "__main__":
	main()

