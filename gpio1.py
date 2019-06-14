import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT, initial=GPIO.HIGH)

# STEP 1 MCU send command
GPIO.output(2, GPIO.HIGH)
time.sleep(0.050)
GPIO.output(2, GPIO.LOW)
time.sleep(0.020)
GPIO.setup(2, GPIO.IN, GPIO.PUD_UP)
# STEP 2: sensor response
GPIO.wait_for_edge(2, GPIO.FALLING)
t1 = time.time()
GPIO.wait_for_edge(2, GPIO.RISING)
t2 = time.time()
print("step2")
if abs(t2-t1-0.000080) < 0.000040:
    print("sensor response!")

while True:
    time.sleep(1)