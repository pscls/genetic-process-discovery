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
    return sorted(models, key=lambda model: evaluate_model(model, symbol_sequences, models))

# Evaluation


def evaluate_model(model, symbol_sequences, models):
    return random.randint(1, 100)

    # Strategies:
    #   Behavioral Appropriateness
    #   Token-Replay
    #   Alignment

    value1 = token_replay_on_symbol_sequences(model, symbol_sequences)
    value2 = token_replay_on_all_estimated_traces(model, models)
    return value1

# IDEA 1


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
