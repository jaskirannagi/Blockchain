import serial
import time
import binascii
from struct import *
port="/dev/ttyAMA0"
baudrate=115200
ser=serial.Serial(port,baudrate)
startbyte="\x7e"

APIframebyte="\x10\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x7D\x31"

	
def unescape(num):
	escbyte=0
	if ord(num)==0x31:
		escbyte=0x11
		return escbyte
		
	if ord(num)==0x33:
		escbyte=0x13
		return escbyte
		
	if ord(num)==0x5D:
		escbyte=0x7D
		return escbyte
		
	if ord(num)==0x5E:
		escbyte=0x7E
		return escbyte
			
def escape(num):
	valbyte=0
	if ord(num)==0x11:
		valbyte=0x31
		
		
	if ord(num)==0x13:
		valbyte=0x33
		
	if ord(num)==0x7D:
		valbyte=0x5D
		
	if ord(num)==0x7E:
		valbyte=0x5E
		
	else:
		return pack("B",ord(num))
		
	return pack('BB',0x7D,valbyte)
	
def APIframefunc(data,opt):
	#opt:
	#0=(plan) go through each character to find the escape byte
	#1=return packetlength
	#2=return checksum
	binascii.hexlify(data)
	' '.join(binascii.hexlify(ch) for ch in data)
	if opt==0:
		msgEsc=""
		escbyte=""
		for ch in data:
			escbyte=escape(ch)
			if ord(ch)==0x7D:
				escbyte='\x7D\x5D'
			msgEsc+=escbyte
		return msgEsc	
	if opt==1:
		MSBLen=0x00
		LSBLen=0x0E

		for ch in data:
			if ord(ch)==0x7D:
				continue
			if LSBLen==0xFF:
				LSBLen=0
				MSBLen+=1
				
			LSBLen += 1
			
		return pack('BB', MSBLen, LSBLen)
	if opt==2:
		escp=False
		total=0
		for ch in data:
			
			if ord(ch)==0x7D:
				if escp==False:
					escp=True
					continue
			if escp==True:
				escp=False
				escval=unescape(ch)
				total+=escval
				continue
				
			total += ord(ch)
		checksum= 0xFF - (total & 0xFF)
		return pack('B',checksum)
		
		

while 1:
	msg="Hi Dr John Rigelsford" 
	#validate msgSend checking the escape character(repack with escape)
	msgSend=APIframefunc(msg,0)
	
	StLn=startbyte+APIframefunc(msgSend,1)
	APIframe=APIframebyte+msgSend
	chksum=APIframefunc(APIframe,2)
	TxAPI=StLn+APIframe+chksum
	i=0
	while i< 5:
		ser.write(TxAPI)
		i+=1
		time.sleep(0.1)
