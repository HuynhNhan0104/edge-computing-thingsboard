from time import sleep
from umqtt.simple import MQTTClient
from machine import Pin
from dht import DHT22
import json
import network

# MQTT 
SERVER = '127.0.0.1'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'LB4oqgfzi0Ulc9ingWun' # access token 
TOPIC_TELEMETRY = 'v1/devices/me/telemetry'
#wifi SSID and password
WIFI_SSID = "NHAN"     
WIFI_PASSWORD = "0123456789"




# connect to the wifi network
def connectWIFI():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID,WIFI_PASSWORD)
    while not wlan.isconnected():
        pass

    print ("wifi connected")  
    print(wlan.ifconfig())
  


connectWIFI()
client = MQTTClient(CLIENT_ID, SERVER)
client.connect()   # Connect to MQTT broker
sensor = DHT22(Pin(15, Pin.IN, Pin.PULL_UP))   # DHT-22 on GPIO 15 (input with internal pull-up resistor)
while True:
    try:
        
        sensor.measure()   # Poll sensor
        temp = sensor.temperature()
        humi = sensor.humidity()
        if isinstance(temp, float) and isinstance(humi, float):  # Confirm sensor results are numeric
            msg = collect_data = {'temperature': temp,'humidity': humi}
            client.publish(TOPIC_TELEMETRY, msg)  # Publish sensor data to MQTT topic
            print(msg)
        else:
            print('Invalid sensor readings.')
    except OSError:
        print('Failed to read sensor.')
    sleep(15*60)