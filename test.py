import network
import time
import gc
from umqtt.simple import MQTTClient
from machine import Pin
import dht

print("free memory before request:", gc.mem_free())

# Fill in your WiFi network name (SSID) and password here:
wifi_ssid = "TP-Link_60B2"
wifi_password = "04613510"

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while not wlan.isconnected():
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

# Fill in your Adafruit IO Authentication and Feed MQTT Topic details
mqtt_host = "10.10.40.30"
#mqtt_username = "syco789"  # Your Adafruit IO username
#mqtt_password = "aio_dyow00H6cr4L8VW5K6fJrK1JsfMX"  # Adafruit IO Key
mqtt_publish_topic = "test"# The MQTT topic for your Adafruit IO Feed
#mqtt_publish_topic_2 = "syco789/feeds/tem"
# Enter a random ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "somethingreallyrandomandunique123"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
    client_id=mqtt_client_id,
    server=mqtt_host
    )

mqtt_client.connect()

# Initialize DHT11 sensor on GPIO 14
dht_sensor = dht.DHT11(Pin(0))

# Publish sensor data to the Adafruit IO MQTT server every 10 seconds
try:
    while True:
        # Read sensor data
        dht_sensor.measure()
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity

        # Publish the data to the topic
        print(f'Publish Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%')
        mqtt_client.publish(mqtt_publish_topic, f'Temperature={temperature:.2f}')
        mqtt_client.publish(mqtt_publish_topic_2, f'Humidity={humidity:.2f}')

        # Delay a bit to avoid hitting the rate limit
        time.sleep(1)
except Exception as e:
    print(f'Failed to publish message: {e}')
    # Add a longer delay before retrying to avoid rapid reconnection attempts
    #time.sleep(10)
finally:
    mqtt_client.disconnect()