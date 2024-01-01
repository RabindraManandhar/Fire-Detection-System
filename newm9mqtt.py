# MQ-9 sensor configuratioimport network
import network
import time
import gc
from umqtt.simple import MQTTClient
from machine import Pin
from machine import ADC, Pin
import dht

print("free memory before request:", gc.mem_free())

# Fill in your WiFi network name (SSID) and password here:
wifi_ssid = "syco"
wifi_password = "syclops789"

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while not wlan.isconnected():
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

# Fill in your Adafruit IO Authentication and Feed MQTT Topic details
mqtt_host = "io.adafruit.com"
mqtt_username = "syclops789"  # Your Adafruit IO username
mqtt_password = "aio_jrbf78WSBaTMRmSdrnljOuHq9SEj"  # Adafruit IO Key
mqtt_publish_topic = "syclops789/feeds/mq9b"# The MQTT topic for your Adafruit IO Feed
#mqtt_publish_topic_2 = "syco789/feeds/tem"
# Enter a random ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "somethingreallyrandomandunique123"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
    client_id=mqtt_client_id,
    server=mqtt_host,
    user=mqtt_username,
    password=mqtt_password)

mqtt_client.connect()

# Initialize DHT11 sensor on GPIO 14
adc_pin = ADC(28)  # Assuming the sensor is connected to ADC pin 0


# Publish sensor data to the Adafruit IO MQTT server every 10 seconds
# Publish sensor data to the Adafruit IO MQTT server every 10 seconds
try:
    while True:
        # Read sensor data
        mq9_sensor_data = adc_pin.read_u16()

        # Publish the data to the topic
        print(f'Publish MQ-9 Sensor Data: {mq9_sensor_data}')
        mqtt_client.publish(mqtt_publish_topic, f'MQ9_Sensor={mq9_sensor_data}')

        # Delay before the next iteration
        time.sleep(10)
except Exception as e:
    print(f'Failed to publish message: {e}')
except Exception as e:
    print(f'Failed to publish message: {e}')
    # Add a longer delay before retrying to avoid rapid reconnection attempts
    #time.sleep(10)
finally:
    mqtt_client.disconnect()