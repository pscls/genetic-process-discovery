import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../src")) # HACKY

from ModelManager import ModelManager
from Gscore import get_g_score
import json
import threading

EXPORT_FITNESS_RESULTS = False

result = {}

true_probs = []
with open("./data/MODEL_DEFINTION.txt") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        [trace, prob] = line.split(" ")
        true_probs.append((trace, float(prob)))

def genetic_magic(symbol_sequences, true_probs):
    # create new model manager
    manager = ModelManager(symbol_sequences, number_of_models=len(symbol_sequences), export_fitness_fnc_results=EXPORT_FITNESS_RESULTS)

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

        for start_index in range(0, len(symbol_sequences), 1000):
            end_index = min(start_index + 1000, len(symbol_sequences))
            print(f"    Start-Sequences: {start_index} - {end_index} (/{len(symbol_sequences)})")

            sequence_result = []
            threads_list = []
    
            for index in range(start_index, end_index, 20):
                partial_symbol_sequences = symbol_sequences[index:index+20]
                t = threading.Thread(target=lambda q, arg1, arg2: q.append(genetic_magic(arg1, arg2)), args=(sequence_result, partial_symbol_sequences, true_probs))
                t.start()
                threads_list.append(t)
            for t in threads_list:
                t.join()

            results_list += sequence_result
    
        result[i] = results_list

# write gscore results to file
fout = open('./data/generated_data/gscore.json', 'w')
fout.write(json.dumps(result))
fout.close()

        