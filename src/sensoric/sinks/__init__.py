from abc import abstractmethod
import numexpr as ne


class Sink:

    def __init__(self):
        self.filter = None

    @abstractmethod
    def write_points(self, data):
        """
        Write datapoints to the sink.
        """
        pass

    def filter_data(self, data):
        if not self.filter:
            return False

        expr = self.filter.format(**data)
        return ne.evaluate(expr)

