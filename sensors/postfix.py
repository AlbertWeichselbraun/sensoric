#!/usr/bin/env python3

import sys
import logging
import subprocess

from bme280 import bme280
from bme280 import bme280_i2c

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
SKIP = 1


def setup():
    pass

def get_measurement_name():
    return 'queue'


def get_sensor_tags():
    """
    Returns:
      All tags attached to the current sensor.
    """
    return {'sensor': 'postfix_queue'}


def get_sensor_fields():
    """
    Returns:
      A key, value mapping of sensor data.
    """
    output = subprocess.check_output(['postqueue', '-p']).decdoe("utf-8")
    # one line per item  header
    queue_size = len(output.splitlines()) - 1
    return dict(postfix_queue=queue_size)


if __name__ == '__main__':
    setup()
    print(get_sensor_fields())
