from abc import abstractmethod
import numexpr as ne
from time import time


class Sink:

    def __init__(self, filter_expr: str = None, requires_flipped: bool = False, data_delay = 0):
        """
        Args:
            filter: filter expression
            requires_flipped:
            data_delay:
        """
        self.flipped = False
        self.last_warn = 0

        self.filter = filter_expr
        self.requires_flipped = requires_flipped
        self.data_delay = data_delay


    @abstractmethod
    def write_points(self, data):
        """
        Write datapoints to the sink.
        """
        pass

    def _apply_filter(self, d):
        try:
            print(self.filter.format(**d))
            return ne.evaluate(self.filter.format(**d))
        except KeyError as e:
            print("~~~", e, d)
            return False

    def filter_data(self, data):
        if not self.filter:
            return False

        print([self._apply_filter(d) for d in data])
        if not any(self._apply_filter(d) for d in data):
            self.flipped = False
            return False

        if (self.requires_flipped and self.flipped) or ((time() - self.last_warn) < self.data_delay):
            return False

        if not self.flipped:
            self.flipped = True
            self.last_warn = time()

        return True
