#!/usr/bin/env python3

import sys
import logging
import subprocess

from bme280 import bme280
from bme280 import bme280_i2c

from sensors import Sensor

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)


class Bme280(Sensor):
    measurement_name = 'bme280'

    def __init__(self):
        """
        Prepares the module for reading sensor data
        """
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

    @property
    def sensor_tags(self):
        return {'sensor': 'bme280x' + hex(bme280_i2c.default_i2c_address)[2:]}

    def get_sensor_fields(self):
        """
        Returns:
          A key, value mapping of sensor data.
        """
        return dict(bme280.read_all()._asdict())


SENSOR = Bme280
if __name__ == '__main__':
    s = SENSOR()
    print(s.get_sensor_fields())
