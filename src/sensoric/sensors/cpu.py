#!/usr/bin/env python3
"""
Sensor used for determining CPU load and temperature.
"""

import os
from os.path import basename
from glob import glob

from sensoric.sensors import Sensor

THERMAL_ZONE = "/sys/devices/virtual/thermal/thermal*"


class Cpu(Sensor):
    measurement_name = 'cpu'
    sensor_tags = {'sensor': 'cpu'}

    @staticmethod
    def _read_temperature(path):
        return int(open(path + "/temp").read()) / 1000

    def get_sensor_fields(self):
        """
        Returns:
            a tuple of temperature, humidity
        """
        fields = {basename(path): self._read_temperature(path) for path in glob(THERMAL_ZONE)}
        fields['load'] = os.getloadavg()[0]  # average load over the last minute.
        return fields


SENSOR = Cpu
if __name__ == '__main__':
    s = SENSOR()
    print("Measuring:", s.get_sensor_fields())
