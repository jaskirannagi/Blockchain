import serial
import time
port="/dev/ttyAMA0"
baudrate=9600
ser=serial.Serial(port,baudrate)


while True:
	ser.write("\x7e")	#send start byte
	ser.write("\x00\x14")	#send length bytes
	ser.write("\x10\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x7D\x31")	#send API frame bytes
	#send message
	ser.write("*haha*")
	#send checksum
	ser.write("\xFC")
	#print indicator
	print("Message is broadcasted!\r\n")
	#sleep for 0.5 sec
	time.sleep(0.5)
