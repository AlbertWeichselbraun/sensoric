#!/usr/bin/env python3
"""
Sensor used for determining virtual memory and swap memory usage.
"""

from urllib.request import urlopen
from json import load

def setup():
    pass


def get_measurement_name():
    return 'power'


def get_sensor_tags():
    return {'sensor': 'power'}


def get_sensor_fields():
    with urlopen('http://192.168.109.35/report') as f:
        return load(f)


if __name__ == '__main__':
    setup()
    print('Measuring:', get_sensor_fields())
