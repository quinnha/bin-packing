from .. import WeightStream
from ..model import Online


class EasiestFit(Online):
    def _process(self, n: int, stream: WeightStream):
        bins = []
        for i in range(n):
            bins.append([])
        for w in stream:
            min_bin = 2**31 - 1
            for i, bin in enumerate(bins):
                if sum(bin) <= min_bin:
                    min_bin = sum(bin)
                    min_index = i

            bins[min_index].append(w)

        return bins


# class EasiestFit(Online):
#     def _process(self, n: int, stream: WeightStream) -> Solution:
#         min = 1e7
#         bins = []
#         for i in range(n):
#             bins.append([])

#         for w in stream:
#             # self._incr_access()
#             bin_index = 0
#             leastW_bin = 0

#             # find the bin with least weight
#             for _ in range(n):
#                 totalWeight = sum(bins[bin_index])
#                 # self._incr_access(len(bins[bin_index]))
#                 if totalWeight < min:
#                     leastW_bin = bin_index
#                     min = totalWeight
#                 bin_index += 1

#             bins[leastW_bin].append(w)

#         return bins
