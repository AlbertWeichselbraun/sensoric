#!/usr/bin/env python3
"""
Sensor used for determining virtual memory and swap memory usage.
"""

from psutil import net_io_counters

from sensoric.sensors import Sensor

IGNORE_DEVICES = ('lo', )
COUNTERS = ('bytes_sent', 'bytes_recv', 'errin', 'errout', 'dropin',
            'dropout')


class Network(Sensor):
    measurement_name = 'net'
    sensor_tags = {'sensor': 'net'}

    def get_sensor_fields(self):
        result = {}
        for netdev, stats in net_io_counters(pernic=True).items():
            if netdev in IGNORE_DEVICES:
                continue

            for counter in COUNTERS:
                key = f'{netdev}_{counter}'
                result[key] = getattr(stats, counter)

        return result


SENSOR = Network
if __name__ == '__main__':
    s = SENSOR()
    print('Measure:', s.get_sensor_fields())
