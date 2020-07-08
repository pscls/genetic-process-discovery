from ModelManager import ModelManager
from Gscore import get_g_score
import sys

# read symbol sequence x from stdin, with one symbol per line
symbol_sequences = []

sequence_file_path = "./data/generated_data/" + sys.argv[1]
with open(sequence_file_path) as file:
    lines = file.readlines()
    for line in lines:
        symbols = line.strip().split(",")

        # check that the start end endsymbol are not use
        assert 'x' not in symbols and 'o' not in symbols

        symbol_sequences.append(symbols)


print(f"[{len(symbol_sequences)} sequences loaded]")

# create to be estimated from symbol_sequence
manager = ModelManager(symbol_sequences, 10)

# run model epochs
manager.run(10)

# show the probability distribution of the different sequences in the model
pred_probs = manager.get_best_model_probility()
# print(pred_probs)


with open("./data/MODEL_DEFINTION.txt") as file:
    lines = file.readlines()
    true_probs = []
    for line in lines:
        line = line.strip()
        [trace, prob] = line.split(" ")
        true_probs.append((trace, float(prob)))
    print(f"G-Score: {get_g_score(pred_probs, true_probs)}")
