import serial
from struct import *

#initialise the xbee port
port="/dev/ttyAMA0"
baudrate=115200
ser=serial.Serial(port,baudrate,timeout=1)
print("Port Opened!\r\n")
print("Received data : \r\n")
#defining the permission to join the character
fillstr=False
escp=False

def unescape(num):
		escbyte=0
		if num==49:
			escbyte=17
			return pack('B', escbyte)
		if num==51:
			escbyte=19
			return pack('B', escbyte)
		if num==93:
			escbyte=125
			return pack('B', escbyte)
		if num==94:
			escbyte=126
			return pack('B', escbyte)
	

while True:
		Msg=""
		rx=""							#initialise empty string for received data
		while True:
			n=ser.inWaiting()			#serial inWaiting reading the number of input buffered bytes
			if n>0:	
				rxbyte=ser.read()			#reading xbee Rx(Din) pin
				
				
					
				if ord(rxbyte)==126:
					if fillstr==False:
						fillstr=True		#allow join in next loop
						continue			#skip the x7E(126) start byte
					else:
						fillstr=False
						break
				
				if ord(rxbyte)==125:		#skip the x7D(125) escaped character
					if escp==False:
						escp=True
						continue
				
				if escp==True:
					escp=False
					rxbyte=unescape(ord(rxbyte))
					
					
								
				if fillstr==True:		
					rx=rx+rxbyte			#join received bytes 
						
							
					
			
		Msg=rx[14:-1]					#filtering the API frame bytes
		print Msg						#printing sent message
