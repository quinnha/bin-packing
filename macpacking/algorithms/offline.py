from .. import Solution, WeightSet
from ..model import Offline
from .online import NextFit as Nf_online
from .online import FirstFit as Ff_online
from .online import BestFit as Bf_online
from .online import WorstFit as Wf_online


class NextFit(Offline):
    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse=True)
        delegation = Nf_online()
        r = delegation((capacity, weights))
        self._incr_access(r["data_accesses"])
        self._incr_comparison(r["comparisons"])
        return r["result"]


class FirstFitDecreasing(Offline):
    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse=True)
        delegation = Ff_online()
        r = delegation((capacity, weights))
        self._incr_access(r["data_accesses"])
        self._incr_comparison(r["comparisons"])
        return r["result"]


class BestFitDecreasing(Offline):
    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse=True)
        delegation = Bf_online()
        r = delegation((capacity, weights))
        self._incr_access(r["data_accesses"])
        self._incr_comparison(r["comparisons"])
        return r["result"]


class WorstFitDecreasing(Offline):
    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse=True)
        delegation = Wf_online()
        r = delegation((capacity, weights))
        self._incr_access(r["data_accesses"])
        self._incr_comparison(r["comparisons"])
        return r["result"]
