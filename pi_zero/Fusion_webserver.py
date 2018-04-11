import sys, getopt
import web
import threading
sys.path.append('.')
import RTIMU
import os.path
import time
import math



SETTINGS_FILE = "RTIMULib"
urls = (
    '/', 'index'
)



class ReadIMUThread(threading.Thread):

    next_due = 0


    def __init__(self):
        # change for multi threading
        super(ReadIMUThread, self).__init__()
        self.__running = threading.Event()
        self.__running.set()
        self.frequency = 0.01


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

    def poll(self):
        try:
            if imu.IMURead():
                # x, y, z = imu.getFusionData()
                # print("%f %f %f" % (x,y,z))
                data = imu.getIMUData()
                fusionPose = data["fusionPose"]
                pitch = math.degrees(fusionPose[0])
                roll = math.degrees(fusionPose[1])
                yaw = math.degrees(fusionPose[2])
                web.pitch = pitch
                web.roll = roll
                web.yaw = yaw
                # print(share_dict["pitch"])
                # print("succed read")
                # print(pitch)
        except Exception as exc:
            print("Read_IMU_Thread Error: %s", exc)


class index:
    def GET(self):
        print(web.pitch)
        return str(web.pitch) + " "+str(web.roll) + " "+str(web.yaw)

        # return str(pitch) + " " + str(roll) + " " + str(yaw)


if __name__ == "__main__":

    app = web.application(urls, globals())
    web.pitch = 0.1
    web.roll = 0.1
    web.yaw = 0.1

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

    # bus.write_byte_data(address, power_mgmt_1, 0)
    # i = imu.IMURead()

    thread_1 = ReadIMUThread()
    thread_1.start()

    app.run()
