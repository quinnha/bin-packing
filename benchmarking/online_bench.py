import pyperf
from macpacking.algorithms.online import (
    WorstBinAlgo,
    NextFit,
    FirstFit,
    BestFit,
    WorstFit,
    RefinedFirstFit,
)
from macpacking.reader import BinppReader
import warnings

warnings.filterwarnings("ignore")

cases = [
    "./_datasets/binpp/N1C1W1/N1C1W1_A.BPP.txt",
    "./_datasets/binpp/N4C1W1/N4C1W1_A.BPP.txt",
    "./_datasets/binpp/N2C1W1/N2C1W1_A.BPP.txt",
    "./_datasets/binpp/N2C3W1/N2C3W1_A.BPP.txt",
    "./_datasets/binpp/N3C3W1/N3C3W1_A.BPP.txt",
    "./_datasets/binpp/N3C3W4/N3C3W4_A.BPP.txt",
]

algorithms = [
    WorstBinAlgo(),
    NextFit(),
    FirstFit(),
    BestFit(),
    WorstFit(),
    RefinedFirstFit(),
]


def run_bench(cases, algorithms):
    runner = pyperf.Runner()

    for algorithm in algorithms:
        for case in cases:
            name = case.split("/")[-1] + " " + type(algorithm).__name__
            data = BinppReader(case).online()
            runner.bench_func(name, algorithm, data)


if __name__ == "__main__":
    run_bench(cases, algorithms)
