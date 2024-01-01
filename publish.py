
import network
import time
from math import sin
import gc
print ("free memory before request:", gc.mem_free())
from umqtt.simple import MQTTClient

wifi_ssid = "TP-Link_60B2"
wifi_password = "04613510"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

mqtt_host = "10.10.40.30"
#mqtt_username = "syclops789"   
#mqtt_password = "aio_jrbf78WSBaTMRmSdrnljOuHq9SEj"   
mqtt_publish_topic = "test"   
mqtt_client_id = "somethingreallyrandomandunique123"

mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host)

mqtt_client.connect()
 
counter = 0
try:
    while True:
  
        sine = sin(counter)
        counter += .8
        
        print(f'Publish {sine:.2f}')
        mqtt_client.publish(mqtt_publish_topic, str(sine))
        
        time.sleep(3)
except Exception as e:
    print(f'Failed to publish message: {e}')
     
    time.sleep(10)  
finally:
    mqtt_client.disconnect()