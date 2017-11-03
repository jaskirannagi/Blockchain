import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT) #blue
GPIO.setup(27,GPIO.OUT) #green
GPIO.setup(22,GPIO.OUT)#red
GPIO.setup(4,GPIO.IN) #switch
while(1):
    if GPIO.input(4):
        GPIO.output(17,GPIO.HIGH)
        GPIO.output(27,GPIO.HIGH)
        GPIO.output(22,GPIO.HIGH)
    else:
        GPIO.output(17,GPIO.LOW)
        GPIO.output(27,GPIO.LOW)
        GPIO.output(22,GPIO.LOW)

