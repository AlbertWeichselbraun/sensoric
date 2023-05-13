"""
A simple sink that logs to stdout used for debugging.
"""
from sensoric.sinks import Sink
from time import ctime


class StdoutSink(Sink):
    def write_points(self, data):
        if not self.filter_data(data):
            print(ctime(), data)
