import time
import RPi.GPIO as GPIO
import threading

# EN, CLK, CW
listRightWheelGPIO = [2, 3, 15]
listLeftWheelGPIO = [10, 9, 11]


class WaterRobotMotorDriver(threading.Thread):
    def __init__(self, listleftwheelgpio, listrightwheelgpio):
        # change for multi threading
        super(WaterRobotMotorDriver, self).__init__()
        self.__running = threading.Event()
        self.__running.set()
        self.listrightwheelgpio = listrightwheelgpio
        self.listleftwheelgpio = listleftwheelgpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.listrightwheelgpio[0], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.listrightwheelgpio[1], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.listrightwheelgpio[2], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.listleftwheelgpio[0], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.listleftwheelgpio[1], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.listleftwheelgpio[2], GPIO.OUT, initial=GPIO.LOW)

        # frequence should between 10-70
        self.freq = 50
        self.RightWheelPWM = GPIO.PWM(self.listrightwheelgpio[1], self.freq)
        self.LeftWheelPWM = GPIO.PWM(self.listleftwheelgpio[1], self.freq)
        self.RightWheelPWM.ChangeDutyCycle(50)
        self.LeftWheelPWM.ChangeDutyCycle(50)
        # self.RightWheelPWM.stop()
        # self.LeftWheelPWM.stop()




    def wheelfreqset(self, freq):
        self.freq = freq
        self.RightWheelPWM.ChangeFrequency(self.freq)
        self.LeftWheelPWM.ChangeFrequency(self.freq)

    def rightwheelenable(self):
        GPIO.output(listRightWheelGPIO[0], GPIO.LOW)

    def leftwheelenable(self):
        GPIO.output(listLeftWheelGPIO[0], GPIO.LOW)

    def rightwheeldisable(self):
        GPIO.output(listRightWheelGPIO[0], GPIO.HIGH)

    def leftwheeldisable(self):
        GPIO.output(listLeftWheelGPIO[0], GPIO.HIGH)

    def forward(self):
        self.rightwheeldisable()
        self.leftwheeldisable()
        self.RightWheelPWM.start(self.freq)
        self.LeftWheelPWM.start(self.freq)
        GPIO.output(self.listleftwheelgpio[2], GPIO.HIGH)
        GPIO.output(self.listrightwheelgpio[2], GPIO.LOW)
        self.rightwheelenable()
        self.leftwheelenable()

    def backward(self):
        self.rightwheeldisable()
        self.leftwheeldisable()
        self.RightWheelPWM.start(self.freq)
        self.LeftWheelPWM.start(self.freq)
        GPIO.output(self.listleftwheelgpio[2], GPIO.LOW)
        GPIO.output(self.listrightwheelgpio[2], GPIO.HIGH)
        self.rightwheelenable()
        self.leftwheelenable()

    def turnright(self):
        self.RightWheelPWM.start(20)
        self.LeftWheelPWM.start(20)
        GPIO.output(self.listleftwheelgpio[2], GPIO.HIGH)
        GPIO.output(self.listrightwheelgpio[2], GPIO.HIGH)
        self.rightwheelenable()
        self.leftwheelenable()

    def turnleft(self):
        self.RightWheelPWM.start(20)
        self.LeftWheelPWM.start(20)
        GPIO.output(self.listleftwheelgpio[2], GPIO.LOW)
        GPIO.output(self.listrightwheelgpio[2], GPIO.LOW)
        self.rightwheelenable()
        self.leftwheelenable()

    def stop(self):
        self.RightWheelPWM.stop()
        self.LeftWheelPWM.stop()
        self.leftwheeldisable()
        self.rightwheeldisable()


if __name__ == "__main__":
    motor = WaterRobotMotorDriver(listLeftWheelGPIO, listRightWheelGPIO)
    motor.forward()
    motor.backward()
    motor.turnleft()
    motor.turnright()
    motor.stop()