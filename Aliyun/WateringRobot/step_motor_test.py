import time
import RPi.GPIO as GPIO

RightWheelEn = 2
RightWheelCLK = 3
RightWheelCW = 15

GPIO.setmode(GPIO.BCM)

GPIO.setup(RightWheelEn, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RightWheelCW, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RightWheelCLK, GPIO.OUT, initial=GPIO.LOW)


RightWheelPWM = GPIO.PWM(RightWheelCLK, 70)
RightWheelPWM.start(70)

GPIO.output(RightWheelCW, GPIO.LOW)
GPIO.output(RightWheelEn, GPIO.LOW)
GPIO.output(RightWheelEn, GPIO.HIGH)

GPIO.output(RightWheelCW, GPIO.HIGH)
GPIO.output(RightWheelEn, GPIO.LOW)


# GPIO.setup(RightWheelCLK, GPIO.OUT)





GPIO.output(RightWheelEn, GPIO.HIGH)
GPIO.output(RightWheelCW, GPIO.HIGH)
# while True:

    # RightWheelPWM.ChangeDutyCycle(dc)
    # RightWheelPWM.ChangeFrequency(f)
    # print(GPIO.input(2))
    # time.sleep(1)
