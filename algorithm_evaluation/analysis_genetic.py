import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../src")) # HACKY

from ModelManager import ModelManager
from Gscore import get_g_score
import json
import threading

result = {}

true_probs = []
with open("./data/MODEL_DEFINTION.txt") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        [trace, prob] = line.split(" ")
        true_probs.append((trace, float(prob)))

def genetic_magic(symbol_sequences, true_probs):
    # take only the first symbol_sequence, should be done for every one later
    symbol_sequence = symbol_sequences[0]
    print(symbol_sequence)
    manager = ModelManager(symbol_sequence, 20)

    # run model epochs
    manager.run(10)

    # show the probability distribution of the different sequences in the model
    pred_probs = manager.get_best_model_probility()

    return get_g_score(pred_probs, true_probs)

for i in range(1, 51):
    print(f"Start-Overlapping: {i}")
    result[i] = []
    with open(f"./data/generated_data/output_{i}.txt") as file:
        lines = file.readlines()
        symbol_sequences = [line.strip().split(",") for line in lines]

        results_list = []
        threads_list = []

        for _ in range(1): #generate n g-scores
            t = threading.Thread(target=lambda q, arg1, arg2: q.append(genetic_magic(arg1, arg2)), args=(results_list, symbol_sequences, true_probs))
            t.start()
            threads_list.append(t)
        completed_threads = 0
        for t in threads_list:
            t.join()

        result[i] = results_list

fout = open('./data/generated_data/gscore.json', 'w')
fout.write(json.dumps(result))
fout.close()

        