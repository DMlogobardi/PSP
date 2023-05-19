from gpiozero import Servo
from time import sleep
import RPi.GPIO as GPIO

def start():
	servo = Servo(2)
	GPIO.setmode(GPIO.BCM)
# The input pin to which the sensor is connected, is declared here.
	GPIO_PIN = 24
	GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	#set a 90 gradi 
	servo.min()
	print("Medio")
	sleep(1)

	#alza la sbarra
	servo.max()
	print("MASSIMO")
	sleep(2)
	fotocell =True
	while fotocell :
		if GPIO.input(GPIO_PIN) == False:
			fotocell=False
			print ("No obstacle")
		else:
			print ("Obstacle detected")
			print ("---------------------------------------")
		sleep(0.5)
	servo.mid()
	print("Medio")
	fotocell =True
	while fotocell :
		if GPIO.input(GPIO_PIN) == False:
			fotocell=False
			print ("No obstacle")
		else:
			print ("Obstacle detected")
			print ("---------------------------------------")
		sleep(0.5)
	#torna giù
	servo.min()
	print("Medio")

start()
#pymysql