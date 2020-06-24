import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import math

averages = []
varianz = []
standard_deviation = []
mins = []
maxs = []
with open("./data/generated_data/gscore.json", "r") as file:
    gscores = json.load(file)

    overlappings = [int(k) for k in gscores.keys()]
    overlappings.sort()


    for overlapping in gscores:
        values = gscores[overlapping]
        average = sum(values)/len(values)
        averages.append(average)

        v = 0
        for v_ in values:
            v += (v_ - average)**2
        v /= len(values)
        varianz.append(v)
        standard_deviation.append(math.sqrt(v))

        mins.append(min(values))
        maxs.append(max(values))

plt.plot(overlappings, varianz, 'ro', markersize=3, label="varianz")
plt.plot(overlappings, averages, 'ko', markersize=3, label="average")
plt.plot(overlappings, mins, 'go', markersize=3, label="min")
plt.plot(overlappings, maxs, 'bo', markersize=3, label="max")
plt.plot(overlappings, standard_deviation, 'yo', markersize=3, label="standard deviation")
plt.axis([min(overlappings) - 1, max(overlappings) + 1, -0.01, 1.01])
plt.xlabel('#Overlapping Sources')

plt.legend(handles=[
    mpatches.Patch(color='red', label='varianz'),
    mpatches.Patch(color='yellow', label='standard deviation'),
    mpatches.Patch(color='green', label='min'),
    mpatches.Patch(color='blue', label='max'),
    mpatches.Patch(color='black', label='average')
])
plt.show()

