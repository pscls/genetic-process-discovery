from ModelManager import ModelManager
import sys

# read symbol sequence x from stdin, with one symbol per line
symbol_sequence = []

sequence_file_path = sys.argv[1]
with open(sequence_file_path) as file:
    lines = file.readlines()
    for line in lines:
        symbol = line.strip()
        if len(symbol) > 0:
            symbol_sequence.append(symbol)


print("({0} symbols loaded)".format(len(symbol_sequence)))

# create to be estimated from symbol_sequence
ModelManager.create_models(symbol_sequence, 1)

# run model epochs
ModelManager.run(5)

# show the probability distribution of the different sequences in the model
print(ModelManager.get_best_model_probility())