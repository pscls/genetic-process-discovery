import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../src")) # HACKY

import base_files_original.mim as mim
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

        for line in lines:
            line = line.strip().split(",")
            m = mim.model(line)
            # estimate model
            K = m.estimate()

            pred_probs = [(trace, prob) for [trace, prob] in m.seqprobs().items()]
            gscore = get_g_score(pred_probs, true_probs)
            result[i].append(gscore)

fout = open('./data/generated_data/gscore.json', 'w')
fout.write(json.dumps(result))
fout.close()

        