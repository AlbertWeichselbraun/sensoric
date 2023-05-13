#!/usr/bin/env python3

"""
sensoric-probe.py [sensor_1|sensor_2|...sensor_n]

probes the given list of sensors.
"""
from sys import argv
from pathlib import Path
from os import getenv
from socket import gethostname
from time import sleep, time
from typing import Dict, List

from .util.config import SensoricConfiguration

"""
TODO:
- add __required_config_flags__ annotation to each modul
"""

HOSTNAME = gethostname()


class Sensoric:

    def __init__(self, configuration_file: Path):
        """
        Setup all sensor modules.
        """
        config = SensoricConfiguration(configuration_file=Path(argv[1]))
        self.sensors = self._init_modules(config.get_sensors())
        self.sinks = self._init_modules(config.get_sink())
        self.batch_size = config.batch_size()

    @staticmethod
    def _init_modules(module_config: Dict[str, Dict]) -> List:
        modules = []
        for sensor, sensor_config in module_config.items():
            sensor = __import__('.' + sensor)
            if sensor_config:
                sensor.setup(**sensor_config)
            else:
                sensor.setup()
            modules.append(sensor)
        return modules

    @staticmethod
    def get_annotated_sensor_data(name, tags, fields):
        """
        Args:
          Converts a list of fields to an InfluxDB measurement.
        """
        tags['host'] = HOSTNAME
        return {
            'measurement': name,
            'tags': tags,
            'fields': fields,
            'time': int(time() * 1E9)
        }

    def watch(self):
        """
        Send an update of all sensor modules to the time series database.
        """
        data = []
        count = 0
        while True:
            data += [Sensoric.get_annotated_sensor_data(m.get_measurement_name(),
                                                        m.get_sensor_tags(),
                                                        m.get_sensor_fields())
                     for m in self.sensors
                     if count % m.skip == 0]

            count = count + 1
            if count % self.batch_size == 0:
                count = 0
                try:
                    print(f'Serializing {len(data)} data points.')
                    for sink in self.sinks:
                        sink.write_points(data)
                    data = []
                except Exception as e:
                    print(e)

            sleep(59)


if __name__ == '__main__':
    import os

    sensoric = Sensoric(Path(argv[1]))
    if sensoric.ignore_proxy and 'http_proxy' in os.environ:
        del os.environ['http_proxy']
    if sensoric.ignore_proxy and 'https_proxy' in os.environ:
        del os.environ['https_proxy']

    sensoric.watch()
