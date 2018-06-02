'''
connect to baidu iothub
use cellphone app send message to this client
'''
import paho.mqtt.client as mqtt
import sys
import uuid

broker = 'swpu_iot_lesson.mqtt.iot.gz.baidubce.com'
port = 1883
username = 'swpu_iot_lesson/temp_sensor'
password = 'URbaan17yK1iLgvyxrs6vbw+pKElDMkqSjRbO1kw8Xk='
clientid = 'test_mqtt_python_' + str(uuid.uuid4())
topic = 'test_topic'


def on_connect(client, userdata, flags, rc):
    print('Connected. Client id is: ' + clientid)
    client.subscribe(topic)
    print('Subscribed to topic: ' + topic)

    # client.publish(topic, 'Message from Baidu IoT demo')
    # print('MQTT message published.')


def on_message(client, userdata, msg):
    msg = str(msg.payload, 'utf-8')
    print('MQTT message received: ' + msg)
    if msg == 'exit':
        sys.exit()

client = mqtt.Client(clientid)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)

print('Connecting to broker: ' + broker)
client.connect(broker, port)

client.loop_forever()
