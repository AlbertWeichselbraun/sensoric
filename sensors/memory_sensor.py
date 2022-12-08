#!/usr/bin/env python3
"""
Sensor used for determining virtual memory and swap memory usage.
"""

from psutil import virtual_memory, swap_memory

SKIP = 1
VIRTUAL_MEM_FIELDS = ('total', 'available', 'buffers', 'cached')
SWAP_MEM_FIELDS = ('total', 'used')


def setup():
    pass


def get_measurement_name():
    return 'memory'


def get_sensor_tags():
    return {'sensor': 'memory'}


def get_sensor_fields():
    mem = virtual_memory()
    result = {field: getattr(mem, field) for field in VIRTUAL_MEM_FIELDS}
    mem = swap_memory()
    result.update({'swap_' + field: getattr(mem, field)
                   for field in SWAP_MEM_FIELDS})
    return result


if __name__ == '__main__':
    setup()
    print('Measuring:', get_sensor_fields())
