import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep
import json

# MQTT 
SERVER = '127.0.0.1'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'LB4oqgfzi0Ulc9ingWun' # access token 
TOPIC_REQUEST = 'v1/devices/me/telemetry'
#wifi SSID and password
WIFI_SSID = 'NHAN'    
WIFI_PASSWORD = '0123456789'

relay = Pin(2, Pin.OUT)

# function active pump or unactive
def unactive_water_pump():
    relay.value(1)

def active_water_pump():
    relay.value(0)


# WiFi connectivity function.
def connectWIFI():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID,WIFI_PASSWORD)
    while not wlan.isconnected():
        pass
    print ("wifi connected")  
    print(wlan.ifconfig())
  
  
#MQTT callback service function
def sub_cb(topic, message): 
    print("Received: ", message.payload.decode("utf-8"))
    try:
        json_obj = json.loads(message.payload)
        if json_obj['method'] == "active_water_pump":
            unactive_water_pump()
            # add response
        elif json_obj['method'] == "unactive_water_pump":
            unactive_water_pump()
        client.publish(message.topic.replace('request', 'response'), message)
    except:
        pass


try:
    connectWIFI()
    client = MQTTClient(CLIENT_ID, SERVER)
    client.connect()   # Connect to MQTT broker
    client.set_callback(sub_cb)
    client.subscribe(TOPIC_REQUEST) 
    print("MQTT connected and ready to receive message")
    while True:
        client.wait_msg()
finally:
    client.disconnect()