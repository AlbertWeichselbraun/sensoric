#!/usr/bin/env python3
"""
Weather sensor based on wttr.in
"""

from os import getenv
from http.client import HTTPSConnection

from sensoric.sensors import Sensor

# only provide one measurement every 5 minutes
SKIP = 5

WEATHER_SERVICE = 'wttr.in'
LOCATIONS = getenv('SENSORIC_WEATHER').lower().split() \
        if getenv('SENSORIC_WEATHER') else None


class Weather(Sensor):
    measurement_name = 'weather'
    sensor_tags = {'sensor': 'weather'}

    def __init__(self, location: str):
        self.location = location

    def get_sensor_fields(self):
        result = {}
        if not self.location:
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
            result[f'{location}_temp'] = float(temp.replace('°C', ''))
            result[f'{location}_humidity'] = float(humidity.replace('%', ''))

        return result


SENSOR = Weather
if __name__ == '__main__':
    s = SENSOR(location='chur')
    print('Measure:', s.get_sensor_fields())
