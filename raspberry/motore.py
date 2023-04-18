from gpiozero import Servo
from time import sleep

def start():
    servo = Servo(2)

    #set a 90 gradi 
    servo.min()
    print("Medio")
    sleep(1)

    #alza la sbarra
    servo.max()
    print("MASSIMO")


    #attesa segnale abbassamento
    sleep(1)

    #torna giù
    servo.min()
    print("Medio")

start()