#!/usr/bin/env python3

import logging
import subprocess

from sensors import Sensor

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)


class Postfix(Sensor):
    measurement_name = 'queue'
    sensor_tags = {'sensor': 'postfix_queue'}

    def get_sensor_fields(self):
        """
        Returns:
          A key, value mapping of sensor data.
        """
        output = subprocess.check_output(['postqueue', '-p']).decdoe("utf-8")
        # one line per item  header
        queue_size = len(output.splitlines()) - 1
        return dict(postfix_queue=queue_size)


SENSOR = Postfix
if __name__ == '__main__':
    s = SENSOR()
    print(s.get_sensor_fields())
