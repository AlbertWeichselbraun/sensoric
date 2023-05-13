"""
A simple sink that logs to stdout used for debugging.
"""
from sinks import Sink
from time import ctime


class NotificationSink(Sink):

    def __init__(self, sink: Sink):
        self.sink = sink

    def write_points(self, data):
        self.sink.write_points(data)
