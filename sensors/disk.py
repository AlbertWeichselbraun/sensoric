#!/usr/bin/env python3
"""
Sensor used for determining virtual memory and swap memory usage.
"""

from psutil import disk_io_counters
from sensors import Sensor

COUNTERS = ('read_bytes', 'write_bytes', 'read_count', 'write_count')


class Disk(Sensor):
    measurement_name = 'disk'
    required_attributes = ('disks', )
    sensor_tags = {'sensor': 'disk'}

    def __init__(self, disks: list[str]):
        self.disks = disks

    def get_sensor_fields(self):
        result = {}
        for disk, stats in disk_io_counters(perdisk=True).items():
            if disk not in self.disks:
                continue

            for counter in COUNTERS:
                key = f'{disk}_{counter}'
                result[key] = getattr(stats, counter)
        return result


SENSOR = Disk
if __name__ == '__main__':
    s = SENSOR(disks=['/dev/sda', ])
    print('Measure:', s.get_sensor_fields())
