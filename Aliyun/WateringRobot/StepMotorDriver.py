import time
import RPi.GPIO as GPIO
import threading
from queue import Queue
import sys

# EN, CLK, CW
listRightWheelGPIO = [2, 3, 15]
listLeftWheelGPIO = [10, 9, 11]


class WaterRobotMotorDriver(threading.Thread):
    def __init__(self, listleftwheelgpio, listrightwheelgpio, queuecmd):
        # change for multi threading
        super(WaterRobotMotorDriver, self).__init__()
        self.__running = threading.Event()
        self.__running.set()
        self.listrightwheelgpio = listrightwheelgpio
        self.listleftwheelgpio = listleftwheelgpio
        self.queuecmd = queuecmd
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.listrightwheelgpio[0], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.listrightwheelgpio[1], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.listrightwheelgpio[2], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.listleftwheelgpio[0], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.listleftwheelgpio[1], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.listleftwheelgpio[2], GPIO.OUT, initial=GPIO.LOW)

        # frequence should between 10-70
        self.freq = 50
        self.duty = 50
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
        if self.freq < 10:
            self.freq = 10
        if self.freq > 60:
            self.freq = 60
        time.sleep(0.1)
        self.rightwheeldisable()
        self.leftwheeldisable()
        time.sleep(0.1)
        self.RightWheelPWM.ChangeFrequency(self.freq)
        self.RightWheelPWM.ChangeDutyCycle(self.duty)
        self.LeftWheelPWM.ChangeFrequency(self.freq)
        self.LeftWheelPWM.ChangeDutyCycle(self.duty)
        self.RightWheelPWM.start(self.duty)
        self.LeftWheelPWM.start(self.duty)


        time.sleep(0.1)
        GPIO.output(self.listleftwheelgpio[2], GPIO.HIGH)
        GPIO.output(self.listrightwheelgpio[2], GPIO.LOW)
        time.sleep(0.1)
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
        # self.RightWheelPWM.ChangeFrequency(0)
        # self.LeftWheelPWM.ChangeFrequency(0)
        self.leftwheeldisable()
        self.rightwheeldisable()

    def run(self):
        while self.__running.isSet():
            print("ent running")
            cmd = self.queuecmd.get()
            if cmd == 'forward':
                print("forward")
                self.forward()
            elif cmd == 'backward':
                self.backward()
            elif cmd == 'turnleft':
                self.turnleft()
            elif cmd == 'turnright':
                self.turnright()
            elif cmd == 'stop':
                print("stop")
                self.stop()
            else:
                cmd = False
            time.sleep(0.1)




if __name__ == "__main__":
    queuecmd = Queue(1)
    thread1 = WaterRobotMotorDriver(listLeftWheelGPIO, listRightWheelGPIO, queuecmd)
    thread1.start()
    # motor = WaterRobotMotorDriver(listLeftWheelGPIO, listRightWheelGPIO, queuecmd)
    # motor.forward()
    # motor.backward()
    # motor.turnleft()
    # motor.turnright()
    # motor.stop()
    while True:
        try:
            msg = input()
        except KeyboardInterrupt:
            sys.exit()
        else:
            if msg == "1":
                queuecmd.put('forward')
            elif msg == "2":
                queuecmd.put('stop')
            else:
                sys.exit()