import random
from base_files.mim import model as Model

def create_offspring(modelA, modelB):
    matrixA = modelA.M
    matrixB = modelB.M
    
    # create new matrix and set each value to the mean of matrixA and MatrixB
    offspring_matrix = matrixA.copy()
    for keyA in offspring_matrix.keys():
        for keyB in offspring_matrix[keyA].keys():
            offspring_matrix[keyA][keyB] = (matrixA[keyA][keyB] + matrixB[keyA][keyB]) / 2 

    # we will not add a symbol sequence for the new Model
    offspring_model = Model("", lambda _, __, ___: offspring_matrix)
    return offspring_model

# Selection
def rank_models(models, symbol_sequences):
    return sorted(models, key=lambda model: evaluate_model(model, symbol_sequences))

# Evaluation
def evaluate_model(model, symbol_sequences):
    
    value = random.randint(1, 100)
    # TODO: Let you magic happen here Anjo...
    #
    # ...your code could be written here :D
    #
    return value