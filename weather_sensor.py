#!/usr/bin/env python3
"""
Weather sensor based on wttr.in
"""

from os import getenv
from http.client import HTTPSConnection

# only provide one measurement every 5 minutes
SKIP = 5

WEATHER_SERVICE = 'wttr.in'
LOCATIONS = getenv('SENSORIC_WEATHER').split() \
        if getenv('SENSORIC_WEATHER') else None


def setup():
    pass


def get_measurement_name():
    return 'weather'


def get_sensor_tags():
    return {'sensor': 'weather'}


def get_sensor_fields():
    result = {}
    if not LOCATIONS:
        return result

    c = HTTPSConnection(WEATHER_SERVICE)
    for location in LOCATIONS:
        c.request('GET', url=f'/{location}?format=%t;%h')
        response = c.getresponse()
        if response.status == 200:
            pass
        else:
            print(f'WARNING: Cannot obtain weather data from {WEATHER_SERVICE} '
                  f'{response.reason} ({response.status}).')

        data = response.read().decode('utf-8')
        temp, humidity = data.split(';')
        result[f'{location}_temp'] = temp
        result[f'{location}_humidity'] = humidity

    return result


if __name__ == '__main__':
    setup()
    print('Measure:', get_sensor_fields())
