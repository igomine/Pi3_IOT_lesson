import sys
from linkkit import linkkit
import threading
import traceback
import inspect
import time
import logging
from enum import Enum
import StepMotorDriver
from queue import Queue
listRightWheelGPIO = [2, 3, 15]
listLeftWheelGPIO = [10, 9, 11]

# config log
__log_format = '%(asctime)s-%(process)d-%(thread)d - %(name)s:%(module)s:%(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(format=__log_format)


# class EnumRobotState(Enum):
#     Stop = 0
#     Forward = 1
#     Backward = 2
#     TurnLeft = 3
#     TurnRight = 4


class CustomerThing(object):
    def __init__(self):
        self.__linkkit = linkkit.LinkKit(
            host_name="cn-shanghai",
            product_key="a1lg8D42TFs",
            device_name="RobotController",
            device_secret="wi88kgvmAPuoTsydVcmC5JJ8VnYlocNj")
        self.__linkkit.enable_logger(logging.DEBUG)
        self.__linkkit.on_device_dynamic_register = self.on_device_dynamic_register
        self.__linkkit.on_connect = self.on_connect
        self.__linkkit.on_disconnect = self.on_disconnect
        self.__linkkit.on_topic_message = self.on_topic_message
        self.__linkkit.on_subscribe_topic = self.on_subscribe_topic
        self.__linkkit.on_unsubscribe_topic = self.on_unsubscribe_topic
        self.__linkkit.on_publish_topic = self.on_publish_topic
        self.__linkkit.on_thing_enable = self.on_thing_enable
        self.__linkkit.on_thing_disable = self.on_thing_disable
        self.__linkkit.on_thing_event_post = self.on_thing_event_post
        self.__linkkit.on_thing_prop_post = self.on_thing_prop_post
        self.__linkkit.on_thing_prop_changed = self.on_thing_prop_changed
        self.__linkkit.on_thing_call_service = self.on_thing_call_service
        self.__linkkit.on_thing_raw_data_post = self.on_thing_raw_data_post
        self.__linkkit.on_thing_raw_data_arrived = self.on_thing_raw_data_arrived
        self.__linkkit.thing_setup("model.json")
        self.__linkkit.config_device_info("Eth|03ACDEFF0032|Eth|03ACDEFF0031")
        self.__call_service_request_id = 0

        self.ListRobotStateName = ["Stop", "Forward", "Backward", "TurnLeft", "TurnRight"]
        self.ListRobotStateValue = [0]*5
        self.CurRobotState = "Stop"

        # self.listqueuemsg = ['stop']

        # self.CurRobotState = EnumRobotState.Stop
        # self.ListRobotState = [0]*5
        # self.DictRobotState = {
        #     "Stop": 1,
        #     "Forward": 0,
        #     "Backward": 0,
        #     "TurnLeft": 0,
        #     "TurnRight": 0
        # }
        # self.PropPayload = [False]*5

    def report_robotstate(self):
        # self.ListRobotState = [0] * 5
        # self.ListRobotState[self.CurRobotState.value] = 1
        # prop_data = {
        #     "Stop": self.ListRobotState[0],
        #     "Forward": self.ListRobotState[1],
        #     "Backward": self.ListRobotState[2],
        #     "TurnLeft": self.ListRobotState[3],
        #     "TurnRight": self.ListRobotState[4]
        # }
        for i in range(5):
            if self.CurRobotState == self.ListRobotStateName[i]:
                self.ListRobotStateValue[i] = 1
            else:
                self.ListRobotStateValue[i] = 0
        prop_data = {
            "Stop": self.ListRobotStateValue[0],
            "Forward": self.ListRobotStateValue[1],
            "Backward": self.ListRobotStateValue[2],
            "TurnLeft": self.ListRobotStateValue[3],
            "TurnRight": self.ListRobotStateValue[4]
        }
        self.__linkkit.thing_post_property(prop_data)

    def on_device_dynamic_register(self, rc, value, userdata):
        if rc == 0:
            print("dynamic register device success, value:" + value)
        else:
            print("dynamic register device fail, message:" + value)

    def on_connect(self, session_flag, rc, userdata):
        print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))
        # self.report_robotstate()
        # print("report state once")

    def on_disconnect(self, rc, userdata):
        print("on_disconnect:rc:%d,userdata:" % rc)

    def on_topic_message(self, topic, payload, qos, userdata):
        print("on_topic_message:" + topic + " payload:" + str(payload) + " qos:" + str(qos))
        pass

    def on_subscribe_topic(self, mid, granted_qos, userdata):
        print("on_subscribe_topic mid:%d, granted_qos:%s" %
              (mid, str(','.join('%s' % it for it in granted_qos))))
        pass

    def on_unsubscribe_topic(self, mid, userdata):
        print("on_unsubscribe_topic mid:%d" % mid)
        pass

    def on_publish_topic(self, mid, userdata):
        print("on_publish_topic mid:%d" % mid)

    # server change property of device callback
    def on_thing_prop_changed(self, params, userdata):
        print("on_thing_prop_changed params:" + str(params))
        # self.ListRobotStateValue = [0] * 5
        for i in range(5):
            if self.ListRobotStateName[i] in params.keys():
                self.ListRobotStateValue[i] = params[self.ListRobotStateName[i]]
                self.CurRobotState = self.ListRobotStateName[i]
                if params[self.ListRobotStateName[i]] == 1:
                    print("send queue msg")
                    queuecmd.put(self.ListRobotStateName[i])
            else:
                self.ListRobotStateValue[i] = 0
        self.report_robotstate()
        print("report state once")

    def on_thing_enable(self, userdata):
        print("on_thing_enable")
        print("report state once")
        self.report_robotstate()

    def on_thing_disable(self, userdata):
        print("on_thing_disable")

    def on_thing_event_post(self, event, request_id, code, data, message, userdata):
        print("on_thing_event_post event:%s,request id:%s, code:%d, data:%s, message:%s" %
              (event, request_id, code, str(data), message))
        pass

    # device post property to server complete callback
    def on_thing_prop_post(self, request_id, code, data, message,userdata):
        print("on_thing_prop_post request id:%s, code:%d, data:%s message:%s" %
              (request_id, code, str(data), message))

    def on_thing_raw_data_arrived(self, payload, userdata):
        print("on_thing_raw_data_arrived:%s" % str(payload))

    def on_thing_raw_data_post(self, payload, userdata):
        print("on_thing_raw_data_post: %s" % str(payload))

    def on_thing_call_service(self, identifier, request_id, params, userdata):
        print("on_thing_call_service identifier:%s, request id:%s, params:%s" %
              (identifier, request_id, params))
        self.__call_service_request_id = request_id
        pass

    def user_loop(self):
        self.__linkkit.connect_async()
        tips = "1: disconnect\n" +\
               "2 connect&loop\n" +\
               "3 subscribe topic\n" + \
               "4 unsubscribe topic\n" + \
               "5 public topic\n" +\
               ""
        while True:
            try:
                msg = input()
            except KeyboardInterrupt:
                sys.exit()
            else:
                if msg == "1":
                    event_data = {
                        "Forward": 1,
                        "Stop": 0
                    }
                    self.__linkkit.thing_trigger_event(("passEvent", event_data))
                elif msg == "2":
                    prop_data = {
                        "Forward": 1,
                        "Stop": 0
                    }
                    self.__linkkit.thing_post_property(prop_data)
                elif msg == "3":
                    # power_stage value max than tsl define
                    prop_data = {
                        "abs_speed": 11,
                        "power_stage": 120
                    }
                    self.__linkkit.thing_post_property(prop_data)
                elif msg == "4":
                    self.__linkkit.thing_answer_service("attack", self.__call_service_request_id, 200, {})
                else:
                    sys.exit()


if __name__ == "__main__":
    queuecmd = Queue(1)
    # StepMotorDriver.WaterRobotMotorDriver(listLeftWheelGPIO, listRightWheelGPIO, queuecmd)
    thread1 = StepMotorDriver.WaterRobotMotorDriver(listLeftWheelGPIO, listRightWheelGPIO, queuecmd)
    thread1.start()
    custom_thing = CustomerThing()
    custom_thing.user_loop()
