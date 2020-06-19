from ModelManager import ModelManager
from Gscore import get_g_score
import sys

# read symbol sequence x from stdin, with one symbol per line
symbol_sequences = []

sequence_file_path = sys.argv[1]
with open(sequence_file_path) as file:
    lines = file.readlines()
    for line in lines:
        symbols = line.strip().split(",")

        # check that the start end endsymbol are not use
        assert 'x' not in symbols and 'o' not in symbols

        symbol_sequences.append(symbols)
        

print(f"[{len(symbol_sequences)} sequences loaded]")

# create to be estimated from symbol_sequence
ModelManager.create_models(symbol_sequences, 6)

# run model epochs
ModelManager.run(5)

# show the probability distribution of the different sequences in the model
pred_probs = ModelManager.get_best_model_probility()
print(pred_probs)


if sys.argv[2]:
    true_probs = []
    with open(sys.argv[2]) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            [trace, prob] = line.split(" ")
            true_probs.append((trace, float(prob)))
        print(f"G-Score: {get_g_score(pred_probs, true_probs)}")
