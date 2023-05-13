#!/usr/bin/env python3
"""
Sensor used for determining CPU load and temperature.
"""

import os
from os.path import basename
from glob import glob

THERMAL_ZONE = "/sys/devices/virtual/thermal/thermal*"
SKIP = 1


def setup():
    pass


def get_measurement_name():
    return 'cpu'


def get_sensor_tags():
    return {'sensor': 'cpu'}


def _read_temperature(path):
    return int(open(path + "/temp").read()) / 1000


def get_sensor_fields():
    """
    Returns:
        a tuple of temperature, humidity
    """
    fields = {basename(path): _read_temperature(path) for path in glob(THERMAL_ZONE)}
    fields['load'] = os.getloadavg()[0]  # average load over the last minute.
    return fields


if __name__ == '__main__':
    setup()
    print("Measuring:", get_sensor_fields())
