print("Xin chào ThingsBoard")
import random
import paho.mqtt.client as mqttclient
import time
import json

BROKER_ADDRESS = "localhost"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "LB4oqgfzi0Ulc9ingWun"


def set_growth_period(temp_data):
    if temp_data['growth_period'] in ["Nascent stage","Leaf growth stage","Flowering stage","Seed formation stage","Seed ripening stage"]:
        print("Growth period now is " + temp_data['growth_period'] )
        client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    else:
        print("Entered growth period doesnot exist \n")

#code for mqtt connection

def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def on_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    try:
        json_obj = json.loads(message.payload)
        if  json_obj['method'] == "sendCommand":
            temp_data = {'growth_period': True}
            temp_data['growth_period'] = json_obj['params']['command']
            set_growth_period(temp_data)
            client.publish(message.topic.replace('request', 'response'))

    except:
        pass
    '''
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass
    '''

def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = on_message


client.publish('v1/devices/me/attributes', json.dumps({'growth_period': 'Nascent stage'}), 1)
try:
    while(True):
        time.sleep(30)
except KeyboardInterrupt:
    pass