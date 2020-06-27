import random
import sys
from base_files_edited.mim import model as Model


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
    return offspring_model

# Selection


def rank_models(models, symbol_sequences):
    # TODO: We could think about implement a tournament process here
    return sorted(models, key=lambda model: evaluate_model(model, symbol_sequences, models), reverse=True)

# Evaluation


def evaluate_model(model, symbol_sequences, models):
    # value = random.randint(1, 100)

    # Strategies:
    #   Behavioral Appropriateness
    #   Token-Replay
    #   Alignment

    # value = token_replay_on_symbol_sequences(model, symbol_sequences)
    # value = token_replay_on_all_estimated_traces(model, models)
    value = overall_trace_probabilities(model, models)
    return value

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
