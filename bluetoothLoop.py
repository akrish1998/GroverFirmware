from __future__ import print_function
import time
import math
import serial
import unittest
from roboclaw import Roboclaw
import bluetooth

def main():

	#0x80 -> 128 -> roboclaw #1 wheels 4 & 5 for wheel spin
	#0x81 -> 129 -> roboclaw #2 wheels 6 & 7 for wheel spin
	#0x82 -> 130 -> roboclaw #3 wheels 8 & 9 for wheel spin
	#0x83 -> 131 -> roboclaw #4 wheels 4 & 6 for wheel rotation
	#0x84 -> 132 -> roboclaw #5 wheels 7 & 9 for wheel rotation

	rc = Roboclaw("/dev/ttyS0",115200)
	rc.Open()
	address = [0x80,0x81,0x82,0x83,0x84]

	#target_name = "My Phone"
	#target_address = None

	#nearby_devices = bluetooth.discover_devices()

	#print(len(nearby_devices))

	#for bdaddr in nearby_devices:
		#print(bluetooth.lookup_name(bdaddr))
		#print("In loop")

	#"BLUETOOTH_SOCKET_CONFIG" : 
	#{
		#"UUID"    : "94f39d29-7d6d-437d-973b-fba39e49d4ee",
		#"name"    : "raspberrypi",
		#"timeout" : 1
	#}

	#BLUETOOTH SETUP
	bt_sock = None

	server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	server_sock.bind(("", bluetooth.PORT_ANY))
	server_sock.listen(1)

	port = server_sock.getsockname()[1]

	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	name = "raspberrypi"

	bluetooth.advertise_service( server_sock, name,
					   service_id = uuid,
					   service_classes = [uuid, bluetooth.SERIAL_PORT_CLASS],
					   profiles = [bluetooth.SERIAL_PORT_PROFILE],
					   )
	
	print("waiting for connection on RFCOMM channel")
	print(port)
	
	client_socket, client_info = server_sock.accept()
	client_socket.setblocking(0)
	
	print("Accepted connection")
	print(client_info)

	bt_sock = client_socket
	bt_sock.settimeout(1)

	#READING COMMANDS
	try:
		sockData = bt_sock.recv(1024)
		
		if (sockData[0] < 0):
			print("Moving backwards!")
			moveBackward(30, 2)
		elif (sockData[0] > 0):
			print("Moving forwards!")
			moveForward(30, 2)
		else:
			print("Stopping!")
			stopAll()
	except:
		print("Unable to process data from App!")
		pass

	#CLOSING CONNECTION
	try:
		bt_sock.send('0')
		time.sleep(0.25)
		bt_sock.close()
	except:
		print("Unable to successfully close socket!")
		pass

def moveForward(speed, timer):
	speed = int(speed)
	timer = float(timer)

	rc.ForwardM1(address[RC1], speed)
	rc.ForwardM2(address[RC1], speed)
	rc.ForwardM1(address[RC2], speed)
	rc.ForwardM2(address[RC2], speed)
	rc.ForwardM1(address[RC3], speed)
	rc.ForwardM2(address[RC3], speed)
	
	time.sleep(int(timer))
	
	rc.ForwardM1(address[RC1], 0)
	rc.ForwardM2(address[RC1], 0)
	rc.ForwardM1(address[RC2], 0)
	rc.ForwardM2(address[RC2], 0)
	rc.ForwardM1(address[RC3], 0)
	rc.ForwardM2(address[RC3], 0)

	return 0

def moveBackward(speed, timer):
	speed = int(speed)
	timer = float(timer)

	rc.BackwardM1(address[RC1], speed)
	rc.BackwardM2(address[RC1], speed)
	rc.BackwardM1(address[RC2], speed)
	rc.BackwardM2(address[RC2], speed)
	rc.BackwardM1(address[RC3], speed)
	rc.BackwardM2(address[RC3], speed)
	
	time.sleep(int(timer))
	
	rc.BackwardM1(address[RC1], 0)
	rc.BackwardM2(address[RC1], 0)
	rc.BackwardM1(address[RC2], 0)
	rc.BackwardM2(address[RC2], 0)
	rc.BackwardM1(address[RC3], 0)
	rc.BackwardM2(address[RC3], 0)

	return 0

def stopAll():

	rc.ForwardM1(address[RC1], 0)
	rc.ForwardM2(address[RC1], 0)
	rc.ForwardM1(address[RC2], 0)
	rc.ForwardM2(address[RC2], 0)
	rc.ForwardM1(address[RC3], 0)
	rc.ForwardM2(address[RC3], 0)

	rc.BackwardM1(address[RC1], 0)
	rc.BackwardM2(address[RC1], 0)
	rc.BackwardM1(address[RC2], 0)
	rc.BackwardM2(address[RC2], 0)
	rc.BackwardM1(address[RC3], 0)
	rc.BackwardM2(address[RC3], 0)

	return 0

if __name__ == "__main__":
	main()

