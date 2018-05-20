import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

GPIO.output(2, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)

while True:
    GPIO.output(3, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(3, GPIO.LOW)
    time.sleep(1)