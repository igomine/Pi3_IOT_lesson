import time
import random
import json
import os.path
import sys
import numpy


sys.path.append('./')
from hx711 import HX711


referenceUnit = 1
def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()


hx = HX711(18, 17)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)
hx.reset()
# hx.tare()

init_data = {"sensor_value": "0.0"}
if os.path.exists("/home/pi/Documents/electron_projs/igomine/userData/sensor.json") == False:
    with open("/home/pi/Documents/electron_projs/igomine/userData/sensor.json", 'a+', encoding='utf-8') as fp:
        updata_data = init_data
        json.dump(updata_data, fp)
        fp.close()
    # print("有")
    # with open('/home/pi/Documents/electron_projs/igomine/userData/sensor.json', 'r+', encoding='utf-8') as fp:
    #     updata_data = json.load(fp)
    #     # updata_data["random_value"] = updata_data["random_value"] + 5
    #     updata_data["sensor_value"] = str(float(updata_data["sensor_value"]) + 0.3)
    #     json.dump(updata_data, fp)
    #     fp.close()
# else:
#     print("wu")
#     # with open('../userData/xxx.json', 'w+', encoding='utf-8') as fp:
#     #     fp.close()
#     with open("/home/pi/Documents/electron_projs/igomine/userData/sensor.json", 'a+', encoding='utf-8') as fp:
#         updata_data = init_data
#         json.dump(updata_data, fp)
#         fp.close()
# def KalmanFilter(z, n_iter=20):
#     # 这里是假设A=1，H=1的情况
#
#     # intial parameters
#
#     sz = (n_iter,)  # size of array
#
#     # Q = 1e-5 # process variance
#     Q = 1e-6  # process variance
#     # allocate space for arrays
#     xhat = numpy.zeros(sz)  # a posteri estimate of x
#     P = numpy.zeros(sz)  # a posteri error estimate
#     xhatminus = numpy.zeros(sz)  # a priori estimate of x
#     Pminus = numpy.zeros(sz)  # a priori error estimate
#     K = numpy.zeros(sz)  # gain or blending factor
#
#     R = 0.1 ** 2  # estimate of measurement variance, change to see effect
#
#     # intial guesses
#     xhat[0] = 0.0
#     P[0] = 1.0
#     A = 1
#     H = 1
#
#     for k in range(1, n_iter):
#         # time update
#         xhatminus[k] = A * xhat[k - 1]  # X(k|k-1) = AX(k-1|k-1) + BU(k) + W(k),A=1,BU(k) = 0
#         Pminus[k] = A * P[k - 1] + Q  # P(k|k-1) = AP(k-1|k-1)A' + Q(k) ,A=1
#
#         # measurement update
#         K[k] = Pminus[k] / (Pminus[k] + R)  # Kg(k)=P(k|k-1)H'/[HP(k|k-1)H' + R],H=1
#         xhat[k] = xhatminus[k] + K[k] * (z[k] - H * xhatminus[k])  # X(k|k) = X(k|k-1) + Kg(k)[Z(k) - HX(k|k-1)], H=1
#         P[k] = (1 - K[k] * H) * Pminus[k]  # P(k|k) = (1 - Kg(k)H)P(k|k-1), H=1
#     return xhat

class kalman_filter:
    def __init__(self, Q, R):
        self.Q = Q
        self.R = R

        self.P_k_k1 = 1
        self.Kg = 0
        self.P_k1_k1 = 1
        self.x_k_k1 = 0
        self.ADC_OLD_Value = 0
        self.Z_k = 0
        self.kalman_adc_old = 0

    def kalman(self, ADC_Value):

        self.Z_k = ADC_Value

        if (abs(self.kalman_adc_old - ADC_Value) >= 60):
            self.x_k1_k1 = ADC_Value * 0.382 + self.kalman_adc_old * 0.618
        else:
            self.x_k1_k1 = self.kalman_adc_old;

        self.x_k_k1 = self.x_k1_k1
        self.P_k_k1 = self.P_k1_k1 + self.Q

        self.Kg = self.P_k_k1 / (self.P_k_k1 + self.R)

        kalman_adc = self.x_k_k1 + self.Kg * (self.Z_k - self.kalman_adc_old)
        self.P_k1_k1 = (1 - self.Kg) * self.P_k_k1
        self.P_k_k1 = self.P_k1_k1

        self.kalman_adc_old = kalman_adc

        return kalman_adc

kalman_filter =  kalman_filter(0.1,10)
while True:
    try:
        while not hx.is_ready():
            pass
        val = hx.get_weight(1)

        if val < 0:
            val = 0
        # print(val)
        xhat = kalman_filter.kalman(val)
        print(xhat)
        with open('/home/pi/Documents/electron_projs/igomine/userData/sensor.json', 'r+', encoding='utf-8') as fp:
            updata_data = json.load(fp)
            updata_data["sensor_value"] = str(val)
            fp.seek(0, 0)
            fp.truncate()
            json.dump(updata_data, fp)
            fp.close()
        # hx.power_down()
        # hx.power_up()
        time.sleep(0.5)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()





init_data = {"random_value": "123"}
if os.path.exists("d:/userData/xxx.json"):
    # print("有")
    with open('d:/userData/xxx.json', 'r+', encoding='utf-8') as fp:
        updata_data = json.load(fp)
        # updata_data["random_value"] = updata_data["random_value"] + 5
        updata_data["random_value"] = str(float(updata_data["random_value"]) + 0.3)
        fp.close()
else:
    # print("wu")
    # with open('../userData/xxx.json', 'w+', encoding='utf-8') as fp:
    #     fp.close()
    with open("d:/userData/xxx.json", 'a+', encoding='utf-8') as fp:
        updata_data = init_data
        fp.close()

# with open('./foobar.json', 'r+', encoding='utf-8') as fp:
#     updata_data = json.load(fp)
#     updata_data["random_value"] = updata_data["random_value"] + 5

with open('d:/userData/xxx.json', 'w', encoding='utf-8') as fp:
    json.dump(updata_data, fp)
    fp.close()

print(round(float(updata_data["random_value"]),3))
