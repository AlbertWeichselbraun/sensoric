#!/usr/bin/env python3

'''
influx-probe.py [sensor1|sensor2|...sensorn]

probes the given list of sensors.
'''

from sys import argv, exit
modules = [__import__(module) for module in argv[1:]]

import urllib3
from socket import gethostname
from time import sleep, time
from influxdb import InfluxDBClient

DB_HOST = '192.168.109.8'
DB_PORT = 8428
DB_NAME = 'sensors'
HOSTNAME = gethostname()
BATCH_SIZE = 2


def get_annotated_influxdb_data(name, tags, fields):
    '''
    Args:
      Converts a list of fields to an InfluxDB measurement.
    '''
    tags['host'] = HOSTNAME
    return {
               'measurement': name,
               'tags': tags,
               'fields': fields,
               'time': int(time() * 1E9)
           }


def setup():
    '''
    Setup all sensor modules.
    '''
    for module in modules:
        module.setup()


def update():
    '''
    Send an update of all sensor modules to InfluxDB
    '''
    data = []
    count = 0
    while True:
        data += [ get_annotated_influxdb_data(m.get_measurement_name(),
                                              m.get_sensor_tags(),
                                              m.get_sensor_fields())
                for m in modules]

        sink = InfluxDBClient(host=DB_HOST, port=DB_PORT, database=DB_NAME,
                              timeout=1, retries=1)
        count = count + 1
        if count % BATCH_SIZE == 0:
            count = 0
            try:
                print(f'Serializing {len(data)} data points.')
                sink.write_points(data)
                data = []
            except Exception as e:
                print(e)

        sleep(59)


if __name__ == '__main__':
    import os
    if 'http_proxy' in os.environ:
        del os.environ['http_proxy']
    if 'https_proxy' in os.environ:
        del os.environ['https_proxy']
    setup()
    update()
