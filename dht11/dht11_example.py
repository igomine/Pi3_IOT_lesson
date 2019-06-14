import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# read data using pin 14
instance = dht11.DHT11(pin=2)

while True:
    result = instance.read()
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %d C" % result.temperature)
        print("Humidity: %d %%" % result.humidity)

    time.sleep(0.1)