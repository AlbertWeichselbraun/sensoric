#!/usr/bin/env python3
"""
Sensor used for determining virtual memory and swap memory usage.
"""

from psutil import disk_io_counters

DEVICES = ('sda', 'sdb', 'mmcblk1')
COUNTERS = ('read_bytes', 'write_bytes', 'read_count', 'write_count')

def setup():
    pass


def get_measurement_name():
    return 'disk'


def get_sensor_tags():
    return {'sensor': 'disk'}

def get_sensor_fields():
    result = {}
    for disk, stats in disk_io_counters(perdisk=True).items():
        if disk not in DEVICES:
            continue

        for counter in COUNTERS:
            key = f'{disk}_{counter}'
            result[key] = getattr(stats, counter)

    return result


if __name__ == '__main__':
    setup()
    print('Measure:', get_sensor_fields())
