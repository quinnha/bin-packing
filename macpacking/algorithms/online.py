from .. import Solution, WeightStream
from ..model import Online


class NextFit(Online):
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_index = 0
        solution = [[]]
        remaining = capacity
        for w in stream:
            self._incr_access()
            self._incr_comparison()
            if remaining >= w:
                solution[bin_index].append(w)
                self._incr_access()
                remaining = remaining - w
            else:
                bin_index += 1
                solution.append([w])
                remaining = capacity - w
        return solution


class WorstBinAlgo(Online):
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        allBins = [[w] for w in stream]
        for _ in range(len(allBins)):
            self._incr_access()
            self._incr_comparison()
        return allBins


class FirstFit(Online):
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_index = 0
        bins = [[]]
        remaining = capacity
        for w in stream:
            self._incr_access()
            while bin_index < len(bins):
                self._incr_comparison()
                remaining = capacity - sum(bins[bin_index])
                self._incr_access(len(bins[bin_index]))
                self._incr_access()
                self._incr_comparison()
                if remaining >= w:
                    bins[bin_index].append(w)
                    remaining = remaining - w
                    self._incr_access()
                    break
                bin_index += 1

            # weight doesnt fit, create new bin
            self._incr_comparison()
            if bin_index == len(bins):
                bins.append([w])
                remaining = capacity - w
                self._incr_access()
        return bins


class BestFit(Online):
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bins = [[]]
        remaining = capacity
        for w in stream:
            self._incr_access()
            bin_index = 0
            min = capacity + 1
            tightest_bin = 0

            # find tightest bin suited for the current weight
            for i in range(len(bins)):
                self._incr_comparison()
                remaining = capacity - sum(bins[bin_index])
                self._incr_access(len(bins[bin_index]))
                self._incr_comparison(3)
                if remaining >= w and remaining - w < min:
                    tightest_bin = bin_index
                    min = remaining - w
                bin_index += 1

            # weight doesnt fit, create new bin
            self._incr_comparison()
            if min == capacity + 1:
                bins.append([w])
                remaining = capacity - w
                self._incr_access()
            else:
                bins[tightest_bin].append(w)
                remaining -= w
                self._incr_access()

        return bins


class WorstFit(Online):
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bins = [[]]
        remaining = capacity
        for w in stream:
            self._incr_access()
            bin_index = 0
            most_space = -1
            untight_bin = 0

            # find untightest bin suited for the current weight
            for i in range(len(bins)):
                remaining = capacity - sum(bins[bin_index])
                self._incr_access(len(bins[bin_index]))
                self._incr_comparison(4)
                if remaining >= w and remaining - w > most_space:
                    untight_bin = bin_index
                    most_space = remaining - w
                bin_index += 1

            # weight doesnt fit, create new bin
            self._incr_comparison()
            if most_space == -1:
                bins.append([w])
                remaining = capacity - w
                self._incr_access()
            else:
                bins[untight_bin].append(w)
                remaining -= w
                self._incr_access()

        return bins


class RefinedFirstFit(Online):
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        classes = [[], [], [], []]
        num_class_bin = [0, 0, 0, 0]

        max_ratio = 1
        range1 = 1 / 2
        range2 = 2 / 5
        range3 = 1 / 3
        min_ratio = 0
        b2_counter = 0

        for w in stream:
            self._incr_access(3)
            ratio = w / capacity
            if ratio == 0:
                self._incr_comparison()
                continue
            if ratio > range1 and ratio <= max_ratio:
                self._incr_access()
                self._incr_comparison(2)
                class_num = 0
            elif ratio > range2 and ratio <= range1:
                self._incr_access()
                self._incr_comparison(2)
                class_num = 1
            elif ratio > range3 and ratio <= range2:
                self._incr_access()
                self._incr_comparison(2)
                class_num = 2
                b2_counter += 1
                if (
                    b2_counter % 6 == 0
                    or b2_counter % 7 == 0
                    or b2_counter % 8 == 0
                    or b2_counter % 9 == 0
                ):
                    self._incr_access()
                    self._incr_comparison(4)
                    class_num = 0
            elif ratio > min_ratio and ratio <= range3:
                self._incr_access()
                self._incr_comparison(2)
                class_num = 3

            found_index = 0
            # iterate through all the bins in that class
            while found_index < num_class_bin[class_num]:
                self._incr_access(3)
                self._incr_comparison(2)
                # check if the weight can fit
                if capacity - sum(classes[class_num][found_index]) >= w:
                    break
                found_index += 1

            # fully iterated through the bins of that class, and the weight
            #  did not fit ---> create new bin
            if found_index == num_class_bin[class_num]:
                self._incr_access()
                self._incr_comparison()
                classes[class_num].append([w])
                num_class_bin[class_num] += 1
            else:
                classes[class_num][found_index].append(w)
                self._incr_access(2)

        return classes[0] + classes[1] + classes[2] + classes[3]
