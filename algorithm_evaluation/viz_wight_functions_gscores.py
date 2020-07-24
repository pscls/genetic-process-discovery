import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import math

with open("./data/generated_data/gscore_wight_function.json", "r") as file:
    lines = file.readlines() 

    for line in lines:
        gscores = json.loads(line)
        plt.plot(list(range(len(gscores))), gscores, 'o', markersize=4, color='black',  alpha=0.1)
    
        # for i in range(len(gscores)):
        #     plt.scatter(i, gscores[i])
    
    plt.xticks([0, 5, 10, 15, 19])

    plt.xlabel("List Index")
    plt.ylabel("G-score")
    plt.show()
