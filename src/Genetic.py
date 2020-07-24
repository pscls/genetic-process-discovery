import random
import sys
from base_files_edited.mim import model as Model
from Gscore import get_g_score
from operator import itemgetter
import json


def create_random_model(sequence):
    # first: create a normal model
    model = Model(sequence)
    
    # second: overwrite matrix with a random one
    matrix = model.M

    for keyA in matrix:
        if keyA == Model.BEGIN:
            # we do not want to randomize the start at this point
            continue

        row_sum = 0.0
        for keyB in matrix[keyA]:
            random_value = random.random()
            row_sum += random_value
            matrix[keyA][keyB] = random_value
        
        # normalize matrix
        for keyB in matrix[keyA]:
            matrix[keyA][keyB] /= row_sum

    model.M = matrix
    return model


def create_offspring(modelA, modelB):
    matrixA = modelA.M
    matrixB = modelB.M

    # create new matrix and set each value to the mean of matrixA and MatrixB
    offspring_matrix = matrixA.copy()
    for keyA in offspring_matrix.keys():
        for keyB in offspring_matrix[keyA].keys():
            offspring_matrix[keyA][keyB] = (
                matrixA[keyA][keyB] + matrixB[keyA][keyB]) / 2

    # we will not add a symbol sequence for the new Model
    offspring_model = Model("", lambda _, __, ___: offspring_matrix)

    return mutate(offspring_model, force_mutation=True)

def mutate(model, force_mutation=False):
    model_mutation_prob = 0.3 # probability that a model gets mutated
    value_mutation_prob = 0.3 # probability that a value gets mutated
    value_mutation_range = 0.2 # range of value mutation = [1-x, 1+x]

    if random.random() > model_mutation_prob:
        return model

    mutated_matrix = model.M
    for keyA in mutated_matrix:
        rowsum = 0.0
        
        # mutate values
        for keyB in mutated_matrix[keyA]:
            if random.random() > value_mutation_prob:
                continue
            
            # zero values will stay zero
            mutated_matrix[keyA][keyB] *= random.uniform(1-value_mutation_range, 1+value_mutation_range)
            rowsum += mutated_matrix[keyA][keyB]

        # normalize values after mutation
        if rowsum > 0:
            for keyB in mutated_matrix[keyA]:
                mutated_matrix[keyA][keyB] /= rowsum
    
    model.M = mutated_matrix
    return model

def save_gscore_for_models(models):
    with open("./data/MODEL_DEFINTION.txt") as file:
        lines = file.readlines()
        true_probs = []
        for line in lines:
            line = line.strip()
            [trace, prob] = line.split(" ")
            true_probs.append((trace, float(prob)))
        
        
        gscores = [get_g_score(sorted(model.seqprobs().items(), key=itemgetter(1), reverse=True), true_probs) for model in models]
        fout = open('./data/generated_data/gscore_wight_function.json', 'a+')
        fout.write(json.dumps(gscores) + '\n')
        fout.close()
        
        # print(f"G-Score: {get_g_score(self.get_best_model_probility(), true_probs)}")

# Selection


def rank_models(models, symbol_sequences):
    # TODO: We could think about implement a tournament process here
    ranked_models = sorted(models, key=lambda model: evaluate_model(model, symbol_sequences, models), reverse=True)
    
    save_gscore_for_models(ranked_models)

    return ranked_models

# Evaluation


def evaluate_model(model, symbol_sequences, models):
    # value = random.randint(1, 100)

    # Strategies:
    #   Behavioral Appropriateness
    #   Token-Replay
    #   Alignment

    #value = token_replay_on_symbol_sequences(model, random.choices(symbol_sequences, k=20))
    #value = token_replay_on_all_estimated_traces(model, models)
    # value = overall_trace_probabilities(model, models)
    #value = linked_token_replay(model, random.choices(symbol_sequences, k=20))
    #value = g_score(model, models)
    #value = random.random()
    return value

def g_score(main_model, models):

    main_model_traces = sorted(main_model.seqprobs().items(), key=itemgetter(1), reverse=True)

    score = 0.0
    for model in models:
        model_traces = sorted(model.seqprobs().items(), key=itemgetter(1), reverse=True)
        score += get_g_score(main_model_traces, model_traces)

    return score / len(models)



def linked_token_replay(model, sequences):
    matrix = model.M

    missing = 0.0
    consumed = 0.0
    remaining = 0.0
    produced = 0.0

    for sequence in sequences:
        token_net = {key: [] for key in matrix.keys()}

        token_id = 0
        start_symbol = sequence[0]
        
        for symbol in sequence:
            if symbol == start_symbol: # add a new token into the net
                token_net[symbol].append((token_id, 1))
                token_id += 1
                produced += 1

            if len(token_net[symbol]) == 0:
                missing += 1
                continue

            token_net[symbol] = sorted(token_net[symbol], key=lambda x:x[1], reverse=True)
            token = token_net[symbol].pop(0) # extract token with highest probability

            # if the token has reached the end, we will remove him and all its duplicates from the net
            if matrix[symbol][model.END] > 0:
                consumed += 1
                for token_key in token_net.keys():
                    token_net[token_key] = [_token for _token in token_net[token_key] if _token is not token]
                continue
            
            for other_symbol, probability in matrix[symbol].items():
                if probability > 0:
                    token_net[other_symbol].append((token, probability))

        # count all remaining tokens in the net
        all_remaining_tokens = set()
        for token_key in token_net:
            for _token in token_net[token_key]:
                all_remaining_tokens.add(_token[0])
        remaining += len(all_remaining_tokens)

    f = 1-(missing/consumed)-(remaining/produced)
    return f

# IDEA 1: Token Replay on all unlabeled input sequences


def token_replay_on_symbol_sequences(model, sequences):
    matrix = model.M

    places = dict()

    missing = 0.0
    consumed = 0.0
    remaining = 0.0
    produced = 0.0

    for sequence in sequences:

        # initialize places
        for state in model.D:
            places[state] = 0
            if state == model.BEGIN:
                places['o'] = sys.maxsize

        # iterate through sequence
        for i in range(0, len(sequence)):
            event = sequence[i]
            predecessors = get_predecessors(matrix, event)
            pre_place_prob = 0
            pre_place = 0
            for predecessor in predecessors:
                if predecessors[predecessor] > pre_place_prob:
                    pre_place_prob = predecessors[predecessor]
                    pre_place = predecessor

            if pre_place != 0:
                places[pre_place] -= 1
                places[event] += 1
                consumed += 1
                produced += 1
            else:
                missing += 1
                places[event] += 1
                consumed += 1
                produced += 1

        places[model.BEGIN] = 0
        places[model.END] = 0
        remaining = sum(places.values())

    f = 1-(missing/consumed)-(remaining/produced)
    # print(missing, consumed, remaining, produced)
    # print(f)
    return f

# Idea 2: Token Replay on all estimated traces from the other models


def token_replay_on_all_estimated_traces(model, models):
    matrix = model.M
    estimated_sequences = model.y

    missing_all = 0.0
    consumed_all = 0.0
    remaining_all = 0.0
    produced_all = 0.0

    for sequence in estimated_sequences:
        missing = 0.0
        consumed = 0.0
        remaining = 0.0
        produced = 1

        places = dict()

        # initialize places
        for state in model.D:
            places[state] = 0
            if state == model.BEGIN:
                places['o'] = 1

        # iterate through sequence
        for i in range(0, len(estimated_sequences[sequence])):
            event = estimated_sequences[sequence][i]
            predecessors = get_predecessors(matrix, event)
            pre_place_prob = 0
            pre_place = 0
            for predecessor in predecessors:
                if predecessors[predecessor] > pre_place_prob:
                    pre_place_prob = predecessors[predecessor]
                    pre_place = predecessor

            if pre_place != 0:
                places[pre_place] -= 1
                places[event] += 1
                consumed += 1
                produced += 1
            else:
                missing += 1
                places[event] += 1
                consumed += 1
                produced += 1

        # do it again for the END
        predecessors = get_predecessors(matrix, model.END)
        pre_place_prob = 0
        pre_place = 0
        for predecessor in predecessors:
            if predecessors[predecessor] > pre_place_prob:
                pre_place_prob = predecessors[predecessor]
                pre_place = predecessor
        if pre_place != 0:
            places[pre_place] -= 1
            consumed += 1
        else:
            missing += 1
            consumed += 1

        places[model.BEGIN] = 0
        places[model.END] = 0
        remaining = sum(places.values())

        missing_all = missing
        consumed_all = consumed
        remaining_all = remaining
        produced_all = produced

    f = 1-(missing_all/consumed_all)-(remaining_all/produced_all)
    # print(missing_all, consumed_all, remaining_all, produced_all)
    # print(f)
    return f


def get_predecessors(matrix, event):
    column = dict()
    for row in matrix:
        if (matrix[row][event] != 0.0):
            column[row] = matrix[row][event]
    return column

# IDEA 2: sum of probabilities for a trace in the matrix, for all estimated traces


def overall_trace_probabilities(model, models):
    matrix = model.M

    overall_probability_sum = 0
    probability_count = 0

    for model_instance in models:
        model_probability_sum = 0
        # print('model_instance: ')
        # print(model_instance.y)

        traces = model_instance.y
        for trace_inst in traces:
            trace = traces[trace_inst]
            trace_probability_sum = 0

            for i in range(0, len(trace)):
                event = trace[i]

                previous_event = trace[i-1] if i != 0 else model_instance.BEGIN

                transition_probability = matrix[previous_event][event]

                trace_probability_sum += transition_probability
                probability_count += 1

            # probability of the transition from the last event to the END
            trace_probability_sum += matrix[trace[i-1]
                                            ][model_instance.END]

            model_probability_sum += trace_probability_sum

        overall_probability_sum += model_probability_sum

    relative_probability = overall_probability_sum/probability_count
    return relative_probability

def normalized_overall_trace_probabilities(model, models):
    matrix = model.M

    overall_probability_sum = 0
    model_count = 0

    for model_instance in models:
        model_probability_sum = 0
        trace_count = 0

        traces = model_instance.y
        for trace_inst in traces:
            trace = traces[trace_inst]
            trace_probability_sum = 0

            for i in range(0, len(trace)):
                event = trace[i]

                previous_event = trace[i-1] if i != 0 else model_instance.BEGIN

                transition_probability = matrix[previous_event][event]

                trace_probability_sum += transition_probability
                trace_count += 1

            # probability of the transition from the last event to the END
            trace_probability_sum += matrix[trace[i-1]
                                            ][model_instance.END]

            model_probability_sum += trace_probability_sum

        normalized_model_sum = 1-((1-model_probability_sum)**2)

        overall_probability_sum += normalized_model_sum
        model_count += 1

    relative_probability = overall_probability_sum/model_count
    return relative_probability