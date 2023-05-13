#!/usr/bin/env python3
"""
Fritz!Box sensor based on fritzconnection

https://fritzconnection.readthedocs.io
"""

from fritzconnection.lib.fritzstatus import FritzStatus

from sensoric.sensors import Sensor


COUNTERS = {'bytes_sent': 'bytes_sent',
            'bytes_received': 'bytes_recv',
            'is_connected': 'is_connected',
            'transmission_rate': 'stream',
            'max_byte_rate': 'stream_max'}


class FritzBox(Sensor):
    measurement_name = 'net'
    sensor_tags = {'sensor': 'net'}
    required_attributes = ('address', 'port')

    def __init__(self, address: str, port: int):
        self.fs = FritzStatus(address=address, port=port, use_tls=False, use_cache=True, verify_cache=True)

    def get_sensor_fields(self):
        result = {}
        for soap_call, key in COUNTERS.items():
            value = getattr(self.fs, soap_call)
            if isinstance(value, tuple):
                up, down = value
                result[f'fritz_up{key}'] = int(up)
                result[f'fritz_down{key}'] = int(down)
            else:
                result[f'fritz_{key}'] = int(value)
        return result


SENSOR = FritzBox
if __name__ == '__main__':
    s = SENSOR(address='localhost', port=8000)
    print('Measure:', s.get_sensor_fields())
