import network
from wlan import do_connect
from machine import ADC, Pin
import urequests
import time
import dht
import gc

# Connect to Wi-Fi
do_connect()

# Free up memory
gc.collect()
print("Free memory before request:", gc.mem_free())

# Setup MQ-9B CO sensor
mq9b_adc_pin = 28
mq9b_adc = ADC(mq9b_adc_pin)
flame_adc_pin = 27
flame_adc = ADC(flame_adc_pin)
sensor = dht.DHT11(Pin(0))

def dht_data():
    return {
        'temperature': sensor.temperature,
        'humidity': sensor.humidity
    }

firebase_url = 'https://fire-detect-d2b0b-default-rtdb.firebaseio.com/random.json'
auth_data = {
    "email": "<email>",
    "password": "<password>",
    "returnsecuretoken": True
}

# Authenticate and get localId
auth_response = urequests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=<key>",
                               json=auth_data)
auth_response_data = auth_response.json()
print(auth_response_data)
auth_response.close()
local_id = auth_response_data.get('localId')
print(local_id)

while True:
    try:
        # Read data from MQ-9B CO sensor
        mq9b_gas_value = mq9b_adc.read_u16()
        flame_gas_value = flame_adc.read_u16()

        print("MQ-9B CO Sensor Value:", mq9b_gas_value)
        print("Flame Sensor Value:", flame_gas_value)

        # Get DHT11 sensor data
        dht_data_values = dht_data()

        # Post data to Firebase
        firebase_data = {
            'mq9b_gas_value': mq9b_gas_value,
            'flame_gas_value': flame_gas_value,
            'dht_data': dht_data_values
        }

        response = urequests.post(firebase_url, json=firebase_data)
        data = response.json()
        response.close()
        print(data)

        time.sleep(2)

    except Exception as e:
        print("Error:", e)

    # Delay for readability
    time.sleep(2)