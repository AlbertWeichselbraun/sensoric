"""
A simple sink that logs to stdout used for debugging.
"""
from sinks import Sink
from time import ctime


class StdoutSink(Sink):
    def write_points(self, data):
        print(ctime(), data)
