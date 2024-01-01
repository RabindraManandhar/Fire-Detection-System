import network
from wlan import do_connect
do_connect()
import urequests
import time
from machine import Pin
import dht
import gc
print ("free memory before request:", gc.mem_free())

sensor=dht.DHT11(Pin(0))

def dht_data():
    return {
        'tamperature': sensor.temperature,
        'humidity': sensor.humidity
        }

firebase_url = 'https://fire-detect-d2b0b-default-rtdb.firebaseio.com/random.json'
auth_data={
        "email":"imtiazul.habd@gmail.com",
        "password":"Fire789",
        "returnsecuretoken": True
        }
auth_response=urequests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyC7L2GwAjP11RKjlJd9K-Qdzb1lO6mlBA8",json=auth_data)
auth_response_data=auth_response.json()
print(auth_response_data)
auth_response.close()
local_id=auth_response_data.get('localId')
print(local_id)

while 1:
    dhtdata=dht_data()
    print(dhtdata)
    response=urequests.post(firebase_url,json=dhtdata)
    data=response.json()
    response.close()
    print(data)
    time.sleep(2)


