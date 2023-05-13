from abc import abstractmethod


class Sink:

    @abstractmethod
    def write_points(self, data):
        """
        Write datapoints to the sink.
        """
        pass
