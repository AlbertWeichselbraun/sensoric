#!/usr/bin/env python3

"""
sensoric-probe.py [sensor_1|sensor_2|...sensor_n]

probes the given list of sensors.
"""
from os.path import dirname, join as os_join
from sys import argv, path
from os import getenv
from socket import gethostname
from time import sleep, time

# import all configured sensors
path.append(os_join(dirname(__file__), 'sensors'))
modules = [__import__(module) for module in argv[1:]]
path.append(os_join(dirname(__file__), 'sinks'))

SENSORIC_DB_HOST = getenv('SENSORIC_DB_HOST')
SENSORIC_DB_PORT = getenv('SENSORIC_DB_PORT')
SENSORIC_DB_NAME = getenv('SENSORIC_DB_NAME')
SENSORIC_BATCH_SIZE = int(getenv('SENSORIC_BATCH_SIZE') or 1)
HOSTNAME = gethostname()


class Sensoric:

    def __init__(self, sink):
        """
        Setup all sensor modules.
        """
        self.sink = sink
        for module in modules:
            module.setup()

    @staticmethod
    def get_annotated_sensor_data(name, tags, fields):
        """
        Args:
          Converts a list of fields to an InfluxDB measurement.
        """
        tags['host'] = HOSTNAME
        return {
            'measurement': name,
            'tags': tags,
            'fields': fields,
            'time': int(time() * 1E9)
        }

    def watch(self):
        """
        Send an update of all sensor modules to the time series database.
        """
        data = []
        count = 0
        while True:
            data += [Sensoric.get_annotated_sensor_data(m.get_measurement_name(),
                                                        m.get_sensor_tags(),
                                                        m.get_sensor_fields())
                     for m in modules
                     if count % m.SKIP == 0]

            count = count + 1
            if count % SENSORIC_BATCH_SIZE == 0:
                count = 0
                try:
                    print(f'Serializing {len(data)} data points.')
                    self.sink.write_points(data)
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

    if SENSORIC_DB_HOST and SENSORIC_DB_PORT and SENSORIC_DB_NAME:
        from influxdb import InfluxDBClient
        sink = InfluxDBClient(host=SENSORIC_DB_HOST, port=SENSORIC_DB_PORT,
                              database=SENSORIC_DB_NAME, timeout=1, retries=1)
    else:
        from sinks.stdout import StdoutSink
        sink = StdoutSink()

    sensoric = Sensoric(sink)
    sensoric.watch()
