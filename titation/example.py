import time
import random
import json
import os.path
import sys
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
hx.tare()

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

while True:
    try:
        val = hx.get_weight(5)
        if val < 0:
            val = 0
        print(val)
        with open('/home/pi/Documents/electron_projs/igomine/userData/sensor.json', 'r+', encoding='utf-8') as fp:
            updata_data = json.load(fp)
            updata_data["sensor_value"] = str(val)
            fp.seek(0, 0)
            fp.truncate()
            json.dump(updata_data, fp)
            fp.close()
        hx.power_down()
        hx.power_up()
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
