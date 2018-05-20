import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)


def vibration_callback(channel):
    print("vibration detected!")
    time.sleep(3)
    # return



GPIO.add_event_detect(2, GPIO.FALLING, callback=vibration_callback)

while True:
    pass
    # print(GPIO.input(2))
    # time.sleep(1)
