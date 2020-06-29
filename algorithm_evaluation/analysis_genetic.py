import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../src")) # HACKY

from ModelManager import ModelManager
from Gscore import get_g_score
import json

result = {}

true_probs = []
with open("./data/MODEL_DEFINTION.txt") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        [trace, prob] = line.split(" ")
        true_probs.append((trace, float(prob)))

for i in range(1, 51):
    print(f"Start: {i}")
    result[i] = []
    with open(f"./data/generated_data/output_{i}.txt") as file:
        lines = file.readlines()
        symbol_sequences = [line.strip().split(",") for line in lines]

        for _ in range(3):
            ModelManager.create_models(symbol_sequences, 7)

            # run model epochs
            ModelManager.run(10)

            # show the probability distribution of the different sequences in the model
            pred_probs = ModelManager.get_best_model_probility()

            result[i].append(get_g_score(pred_probs, true_probs))            

fout = open('./data/generated_data/gscore.json', 'w')
fout.write(json.dumps(result))
fout.close()

        