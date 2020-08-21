import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import math
import sys

averages = []
variance = []
standard_deviation = []
mins = []
maxs = []

assert sys.argv[1]
file_name = sys.argv[1]

with open(f"./data/generated/{file_name}", "r") as file:
    gscores = json.load(file)

    overlappings = [int(k) for k in gscores.keys()]
    overlappings.sort()

    for overlapping in gscores:
        values = gscores[overlapping]
        average = sum(values)/len(values)
        averages.append(average)

        v = 0
        for v_ in values:
            v += (100*v_ - 100*average)**2
        v /= len(values)

        variance.append(v/1000)
        standard_deviation.append(math.sqrt(v)/1000)

        mins.append(min(values))
        maxs.append(max(values))

plt.plot(overlappings, averages, 'ko', markersize=3)
plt.axis([min(overlappings) - 1, max(overlappings) + 1, -0.03, 1.03])
plt.xlabel('Number of overlapping sources')
plt.ylabel('G-score')
plt.show()
