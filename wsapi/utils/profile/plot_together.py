"""
One plot for with cache and without cache.
"""
import csv
import matplotlib.pyplot as plt


file1 = 'stats/three_pos_queries_with_cache.csv'
file2 = 'stats/three_pos_queries_without_cache.csv'

def plot_profiler_stats(ax, filename):
    with open(filename, 'r') as ifile:
        statistics = csv.reader(ifile)
        statistics.next()
        count_ar = []
        time_ar = []
        for row in statistics:
            query, count, time = row
            count_ar.append(int(count))
            time_ar.append(float(time))
    ax.plot(count_ar, time_ar, 'o')
    return count_ar, time_ar

figure = plt.figure()
ax = figure.add_subplot(111)
c1, t1 = plot_profiler_stats(ax, file1)
c2, t2 = plot_profiler_stats(ax, file2)

ratio = [b/a for a,b in zip(t1,t2)]

figure2 = plt.figure()
ax2 = figure2.add_subplot(111)
ax2.plot(c1, ratio)

plt.show()

plt.savefig('imgs/three_pos_queries_together.png', dpi=120)
