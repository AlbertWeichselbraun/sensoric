#!/usr/bin/env python3

import Adafruit_DHT as dht

SKIP = 1
SENSOR_ID = dht.DHT22 # DHT22
PIN = 4               # GPIO 4


def setup():
    pass


def get_measurement_name():
    return 'dht22'


def get_sensor_tags():
    return {'sensor': 'dht22'}


def get_sensor_fields():
    """
    Returns:
        a tuple of temperature, humidity
    """
    humidity, temperature = dht.read_retry(SENSOR_ID, PIN)
    return {'humidity': humidity,
            'temperature': temperature}


if __name__ == '__main__':
    setup()
    print("Measuring:", get_sensor_fields())
