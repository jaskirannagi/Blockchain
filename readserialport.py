import serial

port="/dev/ttyAMA0"
baudrate=9600
ser=serial.Serial(port, baudrate, timeout=1.0)
startByte = '\x7e'
initByte = '\x41'
print("Port Opened!\r\n")
print("Received data : \r\n")
printmssg=False
messga=""
finalmsg=""
p=0
while True:

	try:
		n=ser.inWaiting()
		if n>0:
			p=0;
			o=0
			messga=""
			finalmsg=""
			while n>0:
				#if ser.read()==startByte:
				#	print "start byte found!"
				a=ser.read()
				if (ord(a)==42):
					p=p+1	
					if printmssg==True:
						printmssg=False
					else:
						printmssg=True
						
				if printmssg==True:
					if p>=1:
						o=o+1
						if o>1:
							finalmsg=finalmsg+a
				elif p>1:
					break
					
			print finalmsg
				
			
				
									
				
					

					
				
			
	except KeyboardInterrupt:
		break
