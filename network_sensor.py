#!/usr/bin/env python3
"""
Sensor used for determining virtual memory and swap memory usage.
"""

from psutil import net_io_counters

IGNORE_DEVICES = ('lo', )
COUNTERS = ('bytes_sent', 'bytes_recv', 'errin', 'errout', 'dropin',
            'dropout')

def setup():
    pass


def get_measurement_name():
    return 'net'


def get_sensor_tags():
    return {'sensor': 'net'}


def get_sensor_fields():
    result = {}
    for netdev, stats in net_io_counters(pernic=True).items():
        if netdev in IGNORE_DEVICES:
            continue

        for counter in COUNTERS:
            key = f'{netdev}_{counter}'
            result[key] = getattr(stats, counter)

    return result


if __name__ == '__main__':
    setup()
    print('Measure:', get_sensor_fields())
