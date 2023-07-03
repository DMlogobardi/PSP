import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
# The input pin to which the sensor is connected, is declared here.
GPIO_PIN = 24
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# Pause between the output of the result is defined (in seconds)
delayTime = 0.5
print ("Sensor-Test [druecken Sie STRG+C, um den Test zu beenden]")
# Main loop of the program
try:
    while True:
        if GPIO.input(GPIO_PIN) == False:
            print ("No obstacle")
        else:
            print ("Obstacle detected")
            print ("---------------------------------------")
        # Reset + Delay
        time.sleep(delayTime)
    # Clean up after the program has finished
except KeyboardInterrupt:
    GPIO.cleanup()