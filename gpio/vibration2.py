import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)

GPIO.add_event_detect(2, GPIO.FALLING)

count = 0

while True:
    if GPIO.event_detected(2):
        print("vibration detected + %d" % count)
        count += 1
        time.sleep(2)
