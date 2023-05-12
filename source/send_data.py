print("Xin chào ThingsBoard")
import random
import paho.mqtt.client as mqttclient
import time
import json

BROKER_ADDRESS = "127.0.0.1"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "LB4oqgfzi0Ulc9ingWun"


def read_input():
    temp = 16 #random.randint(40, 50)
    humi = 80 #random.randint(20, 80)
    return temp,humi


def subscribed(client, userdata, mid, granted_qos):
    #print("Subscribed...")
    return


def connected(client, usedata, flags, rc):
    if rc == 0:
        #print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")





client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
temp = 45
humi = 50
client.publish('v1/devices/me/attributes', json.dumps({'growth_period': 'Nascent stage'}), 1)
try:
    while(True):
        temp,humi = read_input()
        print("Publish: temperature :" + str (temp)+ ", humidity :" + str(humi))
        collect_data = {'temperature': temp,'humidity': humi}
        client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
        time.sleep(30)
except KeyboardInterrupt:
    pass