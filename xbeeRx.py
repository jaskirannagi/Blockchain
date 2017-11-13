import serial

#initialise the xbee port
port="/dev/ttyAMA0"
baudrate=9600
ser=serial.Serial(port,baudrate)
print("Port Opened!\r\n")
print("Received data : \r\n")
#defining the permission to join the character
fillstr=False
while True:
		n=ser.inWaiting()		#serial inWaiting reading the number of input buffered bytes
		if n>0:
			rx=""					#initialise string for received data
			while True:
				rxbyte=ser.read()		#reading xbee Rx(Din) pin
				
				if ord(rxbyte)==125:		#skip the x7D(125) escaped character
					continue
					
				if ord(rxbyte)==126:
					if fillstr==False:
						fillstr=True	#allow join in next loop
						continue	#skip the x7E(126) start byte
					else:
						fillstr=False	#skip x7E(126) start byte 
							
				if fillstr==True:		
					rx=rx+rxbyte		#join received bytes 
				
				if ord(rxbyte)==126:
					if fillstr==False:
						fillstr=True	#allow join after break
						break		#break loop to retrieve Msg
					
								
						
				
			Msg=rx[14:-1]				#filtering the API frame bytes
			print Msg				#printing sent message
