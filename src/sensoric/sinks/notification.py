"""
A simple sink that logs to stdout used for debugging.
"""
from sensoric.sinks import Sink


class NotificationSink(Sink):

    def __init__(self, sink: Sink):
        self.sink = sink

    def write_points(self, data):
        if not self.filter_data(data):
            self.sink.write_points(data)
