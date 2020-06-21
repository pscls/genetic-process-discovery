import random
import sys
from base_files.mim import model as Model


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
    return sorted(models, key=lambda model: evaluate_model(model, symbol_sequences))

# Evaluation


def evaluate_model(model, symbol_sequences):
    # value = random.randint(1, 100)
    # TODO: Let you magic happen here Anjo...
    #
    # ...your code could be written here :D

    # Strategies:
    #   Behavioral Appropriateness
    #   Token-Replay
    #   Alignment

    # return some number, either float [0, 1] or some integer --> doesn't really matter
    value = token_replay_on_symbol_sequences(model, symbol_sequences)
    return value


def token_replay_on_symbol_sequences(model, sequences):
    matrix = model.M
    # estimated_sequences = model.y

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
    print(missing, consumed, remaining, produced)
    print(f)
    return f


def get_predecessors(matrix, event):
    column = dict()
    for row in matrix:
        if (matrix[row][event] != 0.0):
            column[row] = matrix[row][event]
    return column
