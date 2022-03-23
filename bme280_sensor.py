#!/usr/bin/env python3

import sys
import logging
import subprocess

from bme280 import bme280
from bme280 import bme280_i2c

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

def setup():
    '''
    Prepares the module for reading sensor data
    '''
    output = subprocess.check_output(['i2cdetect', '-y', '1', '0x76', '0x77'])
    if b' 76' in output:
        i2c_address = 0x76
    elif b' 77' in output:
        i2c_address = 0x77
    else:
        logging.error("Cannot find BME280 sensor.")
        sys.exit(-1)

    logging.info("Detected BME280 sensor at address %s.", hex(i2c_address))

    bme280_i2c.set_default_i2c_address(i2c_address)
    bme280_i2c.set_default_bus(1)
    bme280.setup()


def get_measurement_name():
    return 'bme280'


def get_sensor_tags():
    '''
    Returns:
      All tags attached to the current sensor.
    '''
    return {'sensor': 'bme280x' + hex(bme280_i2c.default_i2c_address)[2:]}


def get_sensor_fields():
    '''
    Returns:
      A key, value mapping of sensor data.
    '''
    return dict(bme280.read_all()._asdict())


if __name__ == '__main__':
    setup()
    print(get_sensor_fields())
