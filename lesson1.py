import RPi.GPIO as GPIO
import time

# 1. INIT
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(3, GPIO.IN)


def distance():
    # 2. TRIGGER
    GPIO.output(2, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(2, GPIO.LOW)
    # 3.MEASURE
    if GPIO.wait_for_edge(3, GPIO.RISING, timeout=500):
        t1 = time.time()
    else:
        return False
    if GPIO.wait_for_edge(3, GPIO.FALLING, timeout=500):
        t2 = time.time()
    else:
        return False
    return (t2 - t1)*34000/2

while True:
    time.sleep(0.5)
    x = distance()
    if x != False:
        print("distance:%0.2fcm" % distance())
    else:
        print("too close!")
