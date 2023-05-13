#!/usr/bin/env python3
"""
Fritz!Box sensor based on fritzconnection

https://fritzconnection.readthedocs.io
"""

from os import getenv
from fritzconnection.lib.fritzstatus import FritzStatus

SKIP = 1
FRITZ_HOST = getenv('SENSORIC_FRITZ_HOST')
FRITZ_PORT = int(getenv('SENSORIC_FRITZ_PORT', '49000'))
if not FRITZ_HOST or not FRITZ_PORT:
    print('SENSORIC_FRITZ_HOST and/or SENSORIC_FRITZ_PORT environment variable not set.')
    exit(-1)

COUNTERS = {'bytes_sent': 'bytes_sent',
            'bytes_received': 'bytes_recv',
            'is_connected': 'is_connected',
            'transmission_rate': 'stream',
            'max_byte_rate': 'stream_max'}

fs = FritzStatus(address=FRITZ_HOST, port=FRITZ_PORT, use_tls=False,
                 use_cache=True, verify_cache=True)


def setup():
    pass


def get_measurement_name():
    return 'net'


def get_sensor_tags():
    return {'sensor': 'net'}


def get_sensor_fields():
    result = {}
    for soap_call, key in COUNTERS.items():
        value = getattr(fs, soap_call)
        if isinstance(value, tuple):
            up, down = value
            result[f'fritz_up{key}'] = int(up)
            result[f'fritz_down{key}'] = int(down)
        else:
            result[f'fritz_{key}'] = int(value)

    return result


if __name__ == '__main__':
    setup()
    print('Measure:', get_sensor_fields())
