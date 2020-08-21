import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import math

with open("./data/generated_data/fitness_fnc_results.json", "r") as file:
    lines = file.readlines() 

    for line in lines:
        gscores = json.loads(line)
        plt.plot(list(range(len(gscores))), gscores, 'o', markersize=4, color='black',  alpha=0.05)
    
    plt.xticks([0, 5, 10, 15, 19])

    plt.xlabel("List Index")
    plt.ylabel("G-score")
    plt.show()
