import gc
from machine import Pin, ADC
import utime
from dht import DHT11, InvalidChecksum

# Free up memory
gc.collect()
print("Free memory before setup:", gc.mem_free())

# Setup MQ-9B CO sensor
mq9b_adc_pin = 28
mq9b_adc = ADC(mq9b_adc_pin)

# Setup flame sensor
flame_adc_pin = 27
flame_adc = ADC(flame_adc_pin)

# Setup DHT11 sensor
dht_pin = 0  # GPIO5
dht_sensor_pin = Pin(dht_pin, Pin.OUT, Pin.PULL_DOWN)
dht_sensor = DHT11(dht_sensor_pin)

# Wait 1 second to let the sensors power up
utime.sleep(1)

while True:
    try:
        # Read data from MQ-9B CO sensor
        mq9b_gas_value = mq9b_adc.read_u16()

        # Read data from flame sensor
        flame_gas_value = flame_adc.read_u16()

        print("MQ-9B CO Sensor Value:", mq9b_gas_value)
        print("Flame Sensor Value:", flame_gas_value)

        # Read data from DHT11 sensor
        dht_sensor.measure()
        print("Temperature: {}°C".format(dht_sensor.temperature))
        print("Humidity: {}%".format(dht_sensor.humidity))

        utime.sleep(5)

    except InvalidChecksum:
        print("Checksum from the DHT11 sensor was invalid")

    # Delay for readability
    utime.sleep(2)