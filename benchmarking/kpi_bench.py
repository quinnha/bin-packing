from macpacking.reader import BinppReader
import matplotlib.pyplot as plt
import time
import binpacking
import csv


def compare_KPI(cases, algorithms, algo_type):

    algos = [type(x).__name__ for x in algorithms]

    # Creating data to be graphed
    for case in cases:
        comparisons = []
        data_accesses = []
        operations = []
        bins = []
        runtime = []
        reader = BinppReader(case)

        for algorithm in algorithms:
            start = time.time()
            time.sleep(0.001)
            # Artifically inflating time to avoid
            # rounding down errors (0 runtime)
            if algo_type == "Offline":
                result = algorithm(reader.offline())
            else:
                result = algorithm(reader.online())
            end = time.time() - start - 0.001
            comparisons.append(result["comparisons"])
            data_accesses.append(result["data_accesses"])
            operations.append(result["operations"])
            runtime.append(end * 1000)
            bins.append(len(result["result"]))

        # Graphing KPIs as subplots for each case
        graphs = [data_accesses, comparisons, operations, runtime, bins]
        fig, axs = plt.subplots(2, 3)
        fig.set_size_inches(18.5, 9.5, forward=True)
        fig.tight_layout(pad=10)
        fig.suptitle(case.split("/")[-1] + " " + algo_type, y=0.93)
        axs[0, 0].bar(algos, graphs[0])
        axs[0, 1].bar(algos, graphs[1])
        axs[0, 2].bar(algos, graphs[2])
        axs[1, 0].bar(algos, graphs[3])
        axs[1, 1].bar(algos, graphs[4])

        for rect, ax in zip(algos, axs.ravel()):
            ax.set_xticklabels(algos, rotation=45, ha="right")
            ax.set_xlabel("Algorithm")
            ax.bar_label(ax.containers[0], label_type="edge", padding=5)
            ax.margins(y=0.2)

        axs[0, 0].set_title("Data Accesses")
        axs[0, 1].set_title("Comparisons")
        axs[0, 2].set_title("Operations")
        axs[1, 0].set_title("Runtime (ms)")
        axs[1, 1].set_title("Bins")

        axs[0, 0].set_ylabel("No of Data Accesses")
        axs[0, 1].set_ylabel("No of Comparisons")
        axs[0, 2].set_ylabel("No of Operations")
        axs[1, 0].set_ylabel("Runtime (ms)")

        axs[1, 1].set_xticklabels(algos, rotation=45, ha="right")
        axs[1, 1].set_xlabel("Algorithm")
        temp = axs[1, 1].containers[0]
        axs[1, 1].bar_label(temp, label_type="edge", padding=5)
        axs[1, 1].margins(y=0.2)

        fig.delaxes(axs[1][2])
        plt.show()


# Load Datasets
def load_solutions():

    file = open("./_datasets/jburkardt.csv")
    reader = csv.reader(file)
    jburkardt = {}
    next(reader)

    for row in reader:
        jburkardt[row[0]] = int(row[1])

    file = open("./_datasets/binpp.csv")
    reader = csv.reader(file)
    binpp = {}
    next(reader)

    for row in reader:
        binpp[row[0] + ".BPP.txt"] = int(row[1])

    file = open("./_datasets/binpp-hard.csv")
    reader = csv.reader(file)
    binpp_hard = {}
    next(reader)

    for row in reader:
        binpp_hard[row[0] + ".BPP.txt"] = int(row[-1])

    return jburkardt, binpp, binpp_hard


# Comparing algorithms agaisnt baselines
def compare_baseline(cases, algorithms, algo_type):
    jburkardt, binpp, binpp_hard = load_solutions()
    algos = [type(x).__name__ for x in algorithms]

    new_algos = ["Optimal", "Baseline"] + algos
    bins = []
    for case in cases:
        bins.append([])
        reader = BinppReader(case)

        # Append optimal solutions to be graphed
        bins[-1].append(binpp[case.split("/")[-1]])

        # Append baseline data to be graphed
        capacity, weights = reader.offline()
        bins[-1].append(len(binpacking.to_constant_volume(weights, capacity)))

        for algorithm in algorithms:
            if algo_type == "Offline":
                result = algorithm(reader.offline())
            else:
                result = algorithm(reader.online())

            bins[-1].append(len(result["result"]))

    # Graphing
    fig, axs = plt.subplots(3, 2)
    fig.set_size_inches(19.5, 15.5, forward=True)
    fig.tight_layout(pad=10)
    fig.suptitle("Algorithms vs Bins used (" + algo_type + ")", y=0.93)
    axs[0, 0].bar(new_algos, bins[0])
    axs[0, 1].bar(new_algos, bins[1])
    axs[1, 0].bar(new_algos, bins[2])
    axs[1, 1].bar(new_algos, bins[3])
    axs[2, 0].bar(new_algos, bins[4])
    axs[2, 1].bar(new_algos, bins[5])

    for i, ax in zip(new_algos, axs.ravel()):
        ax.set_xticklabels(new_algos, rotation=45, ha="right")
        ax.set_xlabel("Algorithm")
        ax.set_ylabel("No of Bins")
        ax.bar_label(ax.containers[0], label_type="edge", padding=5)
        ax.margins(y=0.2)

    axs[0, 0].set_title(cases[0].split("/")[-1])
    axs[0, 1].set_title(cases[1].split("/")[-1])
    axs[1, 0].set_title(cases[2].split("/")[-1])
    axs[1, 1].set_title(cases[3].split("/")[-1])
    axs[2, 0].set_title(cases[4].split("/")[-1])
    axs[2, 1].set_title(cases[5].split("/")[-1])

    plt.show()


def compare_baseline_2(cases, algorithms, algo_type):
    # jburkardt, binpp, binpp_hard = load_solutions()
    algos = [type(x).__name__ for x in algorithms]
    new_algos = ["Baseline"] + algos

    bins = []
    for case in cases:
        bins.append([])
        reader = BinppReader(case)

        # Append baseline data to be graphed
        capacity, weights = reader.offline()
        bins[-1].append(len(binpacking.to_constant_bin_number(\
            weights, capacity)))

        for algorithm in algorithms:
            if algo_type == "Offline":
                result = algorithm(reader.offline())
            else:
                result = algorithm(reader.online())

            bins[-1].append(len(result["result"]))

    # Graphing
    fig, axs = plt.subplots(3, 2)
    fig.set_size_inches(19.5, 15.5, forward=True)
    fig.tight_layout(pad=10)
    fig.suptitle("Algorithms vs Bins used (" + algo_type + ")", y=0.93)
    axs[0, 0].bar(new_algos, bins[0])
    axs[0, 1].bar(new_algos, bins[1])
    axs[1, 0].bar(new_algos, bins[2])
    axs[1, 1].bar(new_algos, bins[3])
    axs[2, 0].bar(new_algos, bins[4])
    axs[2, 1].bar(new_algos, bins[5])

    for i, ax in zip(new_algos, axs.ravel()):
        ax.set_xticklabels(new_algos, rotation=45, ha="right")
        ax.set_xlabel("Algorithm")
        ax.set_ylabel("No of Bins")
        ax.bar_label(ax.containers[0], label_type="edge", padding=5)
        ax.margins(y=0.2)

    axs[0, 0].set_title(cases[0].split("/")[-1])
    axs[0, 1].set_title(cases[1].split("/")[-1])
    axs[1, 0].set_title(cases[2].split("/")[-1])
    axs[1, 1].set_title(cases[3].split("/")[-1])
    axs[2, 0].set_title(cases[4].split("/")[-1])
    axs[2, 1].set_title(cases[5].split("/")[-1])

    plt.show()
