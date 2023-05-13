#!/usr/bin/env python3

import Adafruit_DHT as dht

from sensoric.sensors import Sensor

SENSOR_ID = dht.DHT22   # DHT22
PIN = 4                 # GPIO 4


class Ht22(Sensor):
    measurement_name = 'dht22'
    sensor_tags = {'sensor': 'dht22'}

    def get_sensor_fields(self):
        """
        Returns:
            a tuple of temperature, humidity
        """
        humidity, temperature = dht.read_retry(SENSOR_ID, PIN)
        return {'humidity': humidity,
                'temperature': temperature}


SENSOR = Ht22
if __name__ == '__main__':
    s = SENSOR()
    print("Measuring:", s.get_sensor_fields())
