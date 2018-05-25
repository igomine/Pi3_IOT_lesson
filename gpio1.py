import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# GPIO.setup(2, GPIO.OUT)
# GPIO.setup(3, GPIO.OUT)

GPIO.setup((2, 3), GPIO.OUT, initial=GPIO.HIGH)

while True:
    GPIO.output(3, GPIO.HIGH)
    GPIO.output(2, GPIO.LOW)
    time.sleep(1)
    GPIO.output(2, GPIO.HIGH)
    GPIO.output(3, GPIO.LOW)
    time.sleep(1)

