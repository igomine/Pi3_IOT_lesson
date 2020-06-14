import time
import RPi.GPIO as GPIO
import threading


class WaterRobotMotorDriver(threading.Thread):
    def __init__(self, listRightWheelGPIO, listLeftWheelGPIO):
        # change for multi threading
        super(WaterRobotMotorDriver, self).__init__()
        self.__running = threading.Event()
        self.__running.set()



RightWheelEn = 2
RightWheelCLK = 3
RightWheelCW = 15

GPIO.setmode(GPIO.BCM)

GPIO.setup(RightWheelEn, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RightWheelCW, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RightWheelCLK, GPIO.OUT, initial=GPIO.LOW)


RightWheelPWM = GPIO.PWM(RightWheelCLK, 50)
RightWheelPWM.start(50)

GPIO.output(RightWheelEn, GPIO.LOW)
GPIO.output(RightWheelEn, GPIO.HIGH)
GPIO.output(RightWheelEn, GPIO.LOW)

# GPIO.setup(RightWheelCLK, GPIO.OUT)





GPIO.output(RightWheelEn, GPIO.HIGH)
GPIO.output(RightWheelCW, GPIO.HIGH)
# while True:

    # RightWheelPWM.ChangeDutyCycle(dc)
    # RightWheelPWM.ChangeFrequency(f)
    # print(GPIO.input(2))
    # time.sleep(1)
