import network
from wlan import do_connect
import urequests
import time
from machine import ADC, Pin

# Connect to the Wi-Fi network
do_connect()

# Firebase configuration
firebase_url = 'https://fire-detect-d2b0b-default-rtdb.firebaseio.com/mq9_data.json'
auth_data = {
    "email": "imtiazul.habd@gmail.com",
    "password": "Fire789@",
    "returnsecuretoken": True
}

# Authenticate with Firebase
auth_response = urequests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyC7L2GwAjP11RKjlJd9K-Qdzb1lO6mlBA8",
                               json=auth_data)
auth_response_data = auth_response.json()
print(auth_response_data)
auth_response.close()
local_id = auth_response_data.get('localId')
print(local_id)

# MQ-9B sensor configuration
adc_pin = ADC(0)  # Assuming the sensor is connected to ADC pin 0
led_pin = Pin(25, Pin.OUT)  # Assuming an LED is connected to GPIO pin 25

def read_mq9_sensor():
    sensor_value = adc_pin.read_u16()
    return sensor_value

# Main loop to read MQ-9B sensor data and publish to Firebase
while True:
    # Read data from MQ-9B sensor
    mq9_data = read_mq9_sensor()
    print("MQ-9B Sensor Data:", mq9_data)

    # Publish data to Firebase
    firebase_data = {
        'mq9_sensor_data': mq9_data
    }
    response = urequests.post(firebase_url, json=firebase_data)
    data = response.json()
    response.close()
    print(data)

    # Toggle an LED based on sensor data (example)
    if mq9_data > 500:  # Adjust the threshold as needed
        led_pin.on()
    else:
        led_pin.off()

    # Sleep for 2 seconds before the next iteration
    time.sleep(2)