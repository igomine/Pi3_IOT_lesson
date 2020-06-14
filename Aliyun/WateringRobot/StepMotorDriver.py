import time
import RPi.GPIO as GPIO
import threading

# EN, CLK, CW
listRightWheelGPIO = [2, 3, 15]
listLeftWheelGPIO = []


class WaterRobotMotorDriver(threading.Thread):
    def __init__(self, listrightwheelgpio, listleftwheelgpio):
        # change for multi threading
        super(WaterRobotMotorDriver, self).__init__()
        self.__running = threading.Event()
        self.__running.set()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(listrightwheelgpio[0], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(listrightwheelgpio[1], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(listrightwheelgpio[2], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(listleftwheelgpio[0], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(listleftwheelgpio[1], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(listleftwheelgpio[2], GPIO.OUT, initial=GPIO.LOW)
        self.freq = 50
        self.RightWheelPWM = GPIO.PWM(listrightwheelgpio[1], self.freq)
        self.LeftWheelPWM = GPIO.PWM(listleftwheelgpio[1], self.freq)
        self.RightWheelPWM.ChangeDutyCycle(50)
        self.LeftWheelPWM.ChangeDutyCycle(50)
        self.RightWheelPWM.stop()
        self.LeftWheelPWM.stop()

    def wheelfreqset(self, freq):
        self.RightWheelPWM.ChangeFrequency(freq)
        self.LeftWheelPWM.ChangeFrequency(freq)

    def rightwheelenable(self):
        GPIO.output(listRightWheelGPIO[0], GPIO.LOW)

    def leftwheelenable(self):
        GPIO.output(listLeftWheelGPIO[0], GPIO.LOW)

    def rightwheeldisable(self):
        GPIO.output(listRightWheelGPIO[0], GPIO.HIGH)

    def leftwheeldisable(self):
        GPIO.output(listLeftWheelGPIO[0], GPIO.HIGH)

    def forward(self):
        self.RightWheelPWM.start(self.freq)
        self.LeftWheelPWM.start(self.freq)
        self.rightwheelenable()
        self.leftwheelenable()

    def stop(self):
        self.RightWheelPWM.stop()
        self.LeftWheelPWM.stop()
        self.leftwheeldisable()
        self.rightwheeldisable()

