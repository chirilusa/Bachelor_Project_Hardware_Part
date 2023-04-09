import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #Broadcom chip-specific pin numbers
RAIN_PIN = 17
GPIO.setup(RAIN_PIN, GPIO.IN)

for i in range (20):
    # Read digital signal from DO pin
    if GPIO.input(RAIN_PIN) == GPIO.LOW:
        print("It's raining!")
    else:
        print("It's not raining.")

    time.sleep(2)

print ("Stop")