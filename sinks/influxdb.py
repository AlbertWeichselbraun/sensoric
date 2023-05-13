"""
A sink that logs to an InfluxDB.
"""
from influxdb import InfluxDBClient
from sinks import Sink


class NotificationSink(Sink):

    def __init__(self, host: str, port: int, database: str):
        self.influxdb = InfluxDBClient(host=host, port=port, database=database, timeout=1, retries=1)

    def write_points(self, data):
        self.influxdb.write_points(data)
