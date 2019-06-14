import RPi.GPIO as GPIO
import time
# 2 - A, 3 - B, 4 - SW
GPIO.setmode(GPIO.BCM)
GPIO.setup([2, 3, 4], GPIO.IN)
count = 0


def porta_callback(channel):
    if GPIO.input(3):
        global count
        count = (count + 1)
        print("%d" % count)
    else:
        count = (count - 1)
        print("%d" % count)


def portsw_callback(channel):
    print("key pressed!")
GPIO.add_event_detect(2, GPIO.FALLING, callback=porta_callback, bouncetime=50)
GPIO.add_event_detect(4, GPIO.FALLING, callback=portsw_callback, bouncetime=150)

while True:
    time.sleep(1)