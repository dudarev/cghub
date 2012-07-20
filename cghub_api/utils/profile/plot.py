import csv
import matplotlib.pyplot as plt
import sys


def plot_profiler_stats(ifilename, ofilename):
    with open(ifilename, 'r') as ifile:
        statistics = csv.reader(ifile)
        statistics.next()
        count_ar = []
        time_ar = []
        for row in statistics:
            query, count, time = row
            count_ar.append(int(count))
            time_ar.append(float(time))
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.plot(count_ar, time_ar, 'o')
    plt.ylabel('Time [s]', fontsize=20)
    plt.xlabel('Results count', fontsize=20)
    plt.savefig(ofilename, dpi=120)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        plot_profiler_stats(sys.argv[1], sys.argv[2])
    else:
        print("Input and output files aren't specified")

