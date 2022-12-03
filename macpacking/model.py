from abc import ABC, abstractmethod
from typing import Iterator
from . import WeightStream, WeightSet, Solution
from .binpackingmetrics import BinPackMetrics


class BinPacker(ABC):
    pass


class Online(BinPacker):

    access = 0
    comparisons = 0

    def __call__(self, ws: WeightStream):
        capacity, stream = ws
        result = self._process(capacity, stream)
        metrics: BinPackMetrics = {
            "comparisons": self.comparisons,
            "data_accesses": self.access,
            "operations": self.comparisons + self.access,
            "result": result,
        }
        return metrics

    def _incr_comparison(self, n=1):
        self.comparisons += n

    def _incr_access(self, n=1):
        self.access += n

    @abstractmethod
    def _process(self, c: int, stream: Iterator[int]) -> Solution:
        pass


class Offline(BinPacker):

    access = 0
    comparisons = 0

    def __call__(self, ws: WeightSet):
        capacity, weights = ws
        result = self._process(capacity, weights)
        metrics: BinPackMetrics = {
            "comparisons": self.comparisons,
            "data_accesses": self.access,
            "operations": self.comparisons + self.access,
            "result": result,
        }
        return metrics

    def _incr_comparison(self, n=1):
        self.comparisons += n

    def _incr_access(self, n=1):
        self.access += n

    @abstractmethod
    def _process(self, c: int, weights: list[int]) -> Solution:
        pass
