#!/usr/bin/env python3
"""
Sensor used for determining virtual memory and swap memory usage.
"""

from psutil import virtual_memory, swap_memory

from sensors import Sensor

VIRTUAL_MEM_FIELDS = ('total', 'available', 'buffers', 'cached')
SWAP_MEM_FIELDS = ('total', 'used')


class Memory(Sensor):
    measurement_name = 'memory'
    sensor_tags = {'sensor': 'memory'}

    def get_sensor_fields(self):
        mem = virtual_memory()
        result = {field: getattr(mem, field) for field in VIRTUAL_MEM_FIELDS}
        mem = swap_memory()
        result.update({'swap_' + field: getattr(mem, field)
                       for field in SWAP_MEM_FIELDS})
        return result


SENSOR = Memory
if __name__ == '__main__':
    s = SENSOR()
    print('Measuring:', s.get_sensor_fields())
