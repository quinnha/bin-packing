from .. import Solution
from .. import Offline
import binpacking as bp


class ConstantBins(Offline):
    def _process(self, capacity: int, weights: list[int]) -> Solution:
        return bp.to_constant_bin_number(weights, capacity)
