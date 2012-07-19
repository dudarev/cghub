import csv
import matplotlib.pyplot as plt
import sys


def plot_profiler_stats(ifilename, ofilename):
    with open(ifilename, 'r') as ifile:
        statistics = csv.reader(ifile)
        statistics.next()
        figure = plt.figure()
        ax = figure.add_subplot(111)
        for row in statistics:
            query, count, time = row
            ax.plot(int(count), float(time), 'o')
            ax.plot([1, 1], label=query)
        plt.savefig(ofilename, dpi=120)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        plot_profiler_stats(sys.argv[1], sys.argv[2])
    else:
        print("Input and output files aren't specified")

