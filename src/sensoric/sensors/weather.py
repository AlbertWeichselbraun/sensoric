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
    required_attributes = ('locations', )

    def __init__(self, locations: str|list[str]):
        self.locations = [locations, ] if isinstance(locations, str) else locations

    def get_sensor_fields(self):
        result = {}

        c = HTTPSConnection(WEATHER_SERVICE)
        for location in self.locations:
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
    s = SENSOR(locations='chur')
    print('Measure:', s.get_sensor_fields())
