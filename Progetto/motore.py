import RPi.GPIO as GPIO
from time import sleep

def start():
    GPIO.setmode(GPIO.BCM)
    
    # The input pin to which the sensor is connected is declared here.
    GPIO_PIN = 24
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Set servo to 90 degrees
    servo_pin = 2
    GPIO.setup(servo_pin, GPIO.OUT)
    servo_pwm = GPIO.PWM(servo_pin, 50)
    servo_pwm.start(0)
    servo_pwm.ChangeDutyCycle(5.5)  # 90 degrees (adjust as needed)

    motore = True
    i = 0
    while motore:
        fotocell = True
        
        if GPIO.input(GPIO_PIN) == False:
            while fotocell:
                if GPIO.input(GPIO_PIN) == True:
                    sleep(2)
                    servo_pwm.ChangeDutyCycle(11.5)  # Maximum angle (adjust as needed)
                    fotocell = False
        
        elif i == 10:
            servo_pwm.ChangeDutyCycle(11.5)  # Maximum angle (adjust as needed)
            sleep(1)
            
            motore = False
        
        else:
            i = i + 1
            sleep(1)
    
    servo_pwm.stop()
    GPIO.cleanup()
    

#pymysqld