# encoding=utf-8

import time
import sys
import hashlib
import hmac
import base64
import stomp
import ssl


def connect_and_subscribe(conn):
    # 参数说明，请参见AMQP客户端接入说明文档。
    accessKey = "LTAI4Ft5AgtzbHNF9oAwTAgC"
    accessSecret = "tlxa3MLjCd3UPYYu6Iz3DVGqE1iqaN"
    consumerGroupId = "DEFAULT_GROUP"
    # iotInstanceId：购买的实例请填写实例ID，公共实例请填空字符串""。
    iotInstanceId = ""
    clientId = "zaqxsw19831210"
    # 签名方法：支持hmacmd5、hmacsha1和hmacsha256。
    signMethod = "hmacsha1"
    timestamp = current_time_millis()
    # userName组装方法，请参见AMQP客户端接入说明文档。

    userName = clientId + "|authMode=aksign" + ",signMethod=" + signMethod \
                        + ",timestamp=" + timestamp + ",authId=" + accessKey \
                        + ",iotInstanceId=" + iotInstanceId \
                        + ",consumerGroupId=" + consumerGroupId + "|"
    signContent = "authId=" + accessKey + "&timestamp=" + timestamp
    # 计算签名，password组装方法，请参见AMQP客户端接入说明文档。
    password = do_sign(accessSecret.encode("utf-8"), signContent.encode("utf-8"))

    conn.connect(userName, password, wait=True)
    conn.subscribe(destination='/topic/#', id=1, ack='auto')


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        print('received a message "%s"' % message)

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)

    def on_heartbeat_timeout(self):
        print('on_heartbeat_timeout')

    def on_connected(self, headers, body):
        print("successfully connected")


def current_time_millis():
    return str(int(round(time.time() * 1000)))


def do_sign(secret, sign_content):
    m = hmac.new(secret, sign_content, digestmod=hashlib.sha1)
    return base64.b64encode(m.digest()).decode("utf-8")


# 接入域名，请参见AMQP客户端接入说明文档。
conn = stomp.Connection([('1123227406415564.iot-amqp.cn-shanghai.aliyuncs.com', 61614)])
conn.set_ssl(for_hosts=[('1123227406415564.iot-amqp.cn-shanghai.aliyuncs.com', 61614)], ssl_version=ssl.PROTOCOL_TLS)
conn.set_listener('', MyListener(conn))
connect_and_subscribe(conn)

time.sleep(100000)
conn.disconnect()