import serial

port="/dev/ttyAMA0"
baudrate=9600
ser=serial.Serial(port,baudrate)
print("Port Opened!\r\n")
print("Received data : \r\n")
framedata=14
fillstr=False
while True:
		n=ser.inWaiting()
		if n>0:
			i=0
			rx=""
			while True:
				rxbyte=ser.read()
				if ord(rxbyte)==125:
					continue
					
				if fillstr==True:
					rx=rx+rxbyte
				
				if ord(rxbyte)==126:
					if fillstr==True:
						break
					else:
						fillstr=True
						
				
			Msg=rx[framedata:-2]
			print Msg
