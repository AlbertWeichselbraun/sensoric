#!/usr/bin/env python3
"""
Sensor used for determining virtual memory and swap memory usage.
"""

from urllib.request import urlopen
from json import load

from sensors import Sensor


class PowerConsumption(Sensor):
    measurement_name = 'power'
    sensor_tags = {'sensor': 'power'}
    required_attributes = ('url', )

    def __init__(self, url: str):
        self.url = url

    def get_sensor_fields(self):
        with urlopen(self.url) as f:
            return load(f)


SENSOR = PowerConsumption
if __name__ == '__main__':
    s = SENSOR(url='http://192.168.109.35/report')
    print('Measuring:', s.get_sensor_fields())
