import base_files.mim as mim
from Gscore import get_g_score
import json

result = {}

true_probs = []
with open("../sequences.txt") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        [trace, prob] = line.split(" ")
        true_probs.append((trace, float(prob)))

for i in range(1, 51):
    print(f"Start: {i}")
    result[i] = []
    with open(f"./output_{i}.txt") as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip().split(",")
            m = mim.model(line)
            # last_s = None
            # while last_s != m.s:
            #     last_s = m.s
            #     m.estparams()
            #     m.estsources()
            pred_probs = [(trace, prob) for [trace, prob] in m.seqprobs().items()]
            gscore = get_g_score(pred_probs, true_probs)
            result[i].append(gscore)

fout = open('gscore.json', 'w')
fout.write(json.dumps(result))
fout.close()

        