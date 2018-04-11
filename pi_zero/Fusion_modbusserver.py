import sys, getopt
import web
import threading

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import serial
from struct import pack, unpack
import sys
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import RPi.GPIO as GPIO
import threading
import time
import spidev
import itertools
import copy
from RPiMCP23S17.MCP23S17 import MCP23S17
import socket
import os
import queue
import random

SETTINGS_FILE = "RTIMULib"
urls = (
    '/', 'index'
)



class ReadIMUThread(threading.Thread):

    next_due = 0

    def __init__(self, server, slaveid, imu):
        # change for multi threading
        super(ReadIMUThread, self).__init__()
        self.__running = threading.Event()
        self.__running.set()
        self.frequency = 0.01
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        self.server = server
        self.slaveid = slaveid
        self.imu = imu

    def stop(self):
        self.__running.clear()

    def run(self):
        while self.__running.is_set():
            # if self.next_due < time.time():
            #     # print("start poll")
            #     self.poll()
            #     self.next_due = time.time() + self.frequency
            #     # time.sleep(0.05)
            self.poll()
            time.sleep(self.frequency)
        return

    def pitchvalue(self):
        return self.pitch

    def poll(self):
        try:
            slave = self.server.get_slave(self.slaveid)
            if self.imu.IMURead():
                # x, y, z = imu.getFusionData()
                # print("%f %f %f" % (x,y,z))
                data = self.imu.getIMUData()
                fusionPose = data["fusionPose"]
                self.pitch = int(math.degrees(fusionPose[0]))
                self.roll = int(math.degrees(fusionPose[1]))
                self.yaw = int(math.degrees(fusionPose[2]))
                # print("succed read")
                print(self.pitch)
                slave.set_values('READ_INPUT_REGISTERS', 0, self.pitch)
                # values = slave.get_values('READ_INPUT_REGISTERS', 0, 12)
                slave.set_values('READ_INPUT_REGISTERS', 1, self.roll)
                # values = slave.get_values('READ_INPUT_REGISTERS', 0, 12)
                slave.set_values('READ_INPUT_REGISTERS', 2, self.yaw)
                values = slave.get_values('READ_INPUT_REGISTERS', 0, 12)
        except Exception as exc:
            print("Read_IMU_Thread Error: %s", exc)




def main():
    """main"""
    slaveid = 1
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    print("Using settings file " + SETTINGS_FILE + ".ini")
    if not os.path.exists(SETTINGS_FILE + ".ini"):
        print("Settings file does not exist, will be created")

    s = RTIMU.Settings(SETTINGS_FILE)
    imu = RTIMU.RTIMU(s)

    print("IMU Name: " + imu.IMUName())

    if (not imu.IMUInit()):
        print("IMU Init Failed")
        sys.exit(1)
    else:
        print("IMU Init Succeeded")

    # this is a good time to set any fusion parameters

    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)

    poll_interval = imu.IMUGetPollInterval()
    print("Recommended Poll Interval: %dmS\n" % poll_interval)

    try:

        ipaddr = os.popen(
            "ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()
        print("IP:", ipaddr)

        # Create the server
        # server = modbus_tcp.TcpServer(address='192.168.1.111')
        server = modbus_tcp.TcpServer(address=ipaddr)
        logger.info("modbus server running...")
        # logger.info("enter 'quit' for closing the server")

        server.start()

        slave_1 = server.add_slave(slaveid)
        slave_1.add_block('HOLDING_REGISTERS', cst.HOLDING_REGISTERS, 0, 16)
        slave_1.add_block('DISCRETE_INPUTS', cst.DISCRETE_INPUTS, 0, 16)
        slave_1.add_block('READ_INPUT_REGISTERS', cst.READ_INPUT_REGISTERS, 0, 16)
        slave_1.add_block('COILS', cst.COILS, 0, 16)
        # 初始化HOLDING_REGISTERS值
        # 命令行读取COILS的值 get_values 1 2 0 5
        init_value = 0x0
        length = 16
        init_value_list = [init_value]*length
        slave = server.get_slave(1)
        slave.set_values('HOLDING_REGISTERS', 0, init_value_list)

        thread_1 = ReadIMUThread(server, slaveid, imu)
        thread_1.start()
        thread_1.join()

    finally:
        thread_1.stop()
        server.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()