from base_files.mim import model as Model, sortbyvalue
from operator import itemgetter
from Genetic import create_offspring, rank_models
import random
import math


class ModelManager:

    models = []  # array of all models
    symbol_sequences = []

    @staticmethod
    def create_models(symbol_sequences, number_of_models=-1):

        # if no specefic value was passed take the default value of one model per 10 input strings
        if number_of_models < 0:
            number_of_models = math.ceil(len(symbol_sequences) / 10)

        assert len(symbol_sequences) > 0
        assert number_of_models > 0 and number_of_models <= len(
            symbol_sequences)

        ModelManager.symbol_sequences = symbol_sequences

        random.shuffle(symbol_sequences)
        # Intialize Models, each with a different input symbol sequence
        for i in range(number_of_models):
            ModelManager.models.append(Model(symbol_sequences[i]))
        print(f"[{number_of_models} Models Created]")

    # @staticmethod
    # def train_model(model):
    #     model.estparams()
    #     model.estsources()
    #     return

    @staticmethod
    def run(epochs=5):
        assert epochs > 0
        assert len(ModelManager.models) > 0

        for epoch in range(1, epochs + 1):
            print(f"Running Epoch: {epoch}")

            # Estimate traces
            for model in ModelManager.models:
                model.estsources()
                model.estparams()

            # Execute Genetic Step - Selection, Reproduction and Mutation
            # ModelManager.models will be overwritten with next generation models
            ModelManager.darwinism()

            # Assign new input string to each Model for next epoch
            random.shuffle(ModelManager.symbol_sequences)
            for i in range(len(ModelManager.models)):
                model = ModelManager.models[i]
                model.x = ModelManager.symbol_sequences[i]
                model.N = len(model.x)
                model.D = ["o"] + sorted(set(model.x)) + ["x"]

            epochs -= 1
        return

    @staticmethod
    def darwinism():
        next_generation_models = rank_models(
            ModelManager.models, ModelManager.symbol_sequences)
        reproduction_number = 4  # Handle as hyper-param

        assert reproduction_number % 2 == 0  # check for even
        assert reproduction_number >= 2  # check for min
        # assert len(next_generation_models) >= reproduction_number * 1.5 # check if we have enough models to through away and still do reproduction

        # remove weakest models which will the be replaces by offsprings
        next_generation_models = next_generation_models[:-int(
            reproduction_number / 2)]

        for i in range(0, reproduction_number, 2):
            # create offsprings and add them to Models

            offspring = create_offspring(
                next_generation_models[i], next_generation_models[i+1])
            next_generation_models.append(offspring)

        ModelManager.models = next_generation_models

    @staticmethod
    def get_best_model_probility():
        x = ModelManager.models[0].seqprobs()
        return sorted(x.items(), key=itemgetter(1), reverse=True)

    @staticmethod
    def seqprobs():
        results = []
        for model in ModelManager.active_models:
            results.append(model.seqprobs())
        return results

    @staticmethod
    def get_all_model_probabilities():
        probs = ModelManager.seqprobs()
        result = []
        for d_instance in probs:
            result.append(sorted(d_instance.items(),
                                 key=itemgetter(1), reverse=True))
        return result
