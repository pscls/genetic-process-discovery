from base_files_edited.mim import model as Model, sortbyvalue
from operator import itemgetter
from Genetic import create_offspring, rank_models, mutate, create_random_model
from Gscore import get_g_score
import random
import math


class ModelManager:
    models = []
    symbol_sequence = ''
    symbol_sequences = []

    def __init__(self, symbol_sequences, number_of_models=-1, export_fitness_fnc_results=False):

        # if no specefic value was passed take the default value of one model per 10 input strings
        if number_of_models < 0:
            number_of_models = math.ceil(len(symbol_sequences) / 10)

        assert len(symbol_sequences) > 0
        assert number_of_models > 0 and number_of_models <= len(symbol_sequences)

        self.models = []
        self.symbol_sequences = symbol_sequences

        # Intialize Models, each with a different input symbol sequence
        for index in range(number_of_models ):
            self.models.append(Model(self.symbol_sequences[index]))

    def run(self, epochs=5):
        assert epochs > 0
        assert len(self.models) > 0

        current_epoch = 1
        while current_epoch <= epochs:

            # Estimate traces
            for model in self.models:
                model.estsources()
                model.estparams()

            # Execute Genetic Step - Selection, Reproduction and Mutation
            # ModelManager.models will be overwritten with next generation models
            self.darwinism()

            # Assign new input string to each Model for next epoch
            random.shuffle(self.symbol_sequences)
            for i in range(len(self.models)):
                model = self.models[i]
                model.x = self.symbol_sequences[i]
                model.N = len(model.x)
                model.D = ["o"] + sorted(set(model.x)) + ["x"]


            current_epoch += 1

        return

    def darwinism(self):
        next_generation_models = rank_models(
            self.models, self.symbol_sequence)
        reproduction_number = 4  # Handle as hyper-param

        assert reproduction_number % 2 == 0  # check for even
        assert reproduction_number >= 2  # check for min
        assert len(next_generation_models) >= reproduction_number * 1.5 # check if we have enough models to through away and still do reproduction

        # remove weakest models which will the be replaces by offsprings
        next_generation_models = next_generation_models[:-int(
            reproduction_number / 2)]

        for i in range(0, reproduction_number, 2):
            # create offsprings and add them to Models

            offspring = create_offspring(
                next_generation_models[i], next_generation_models[i+1])
            next_generation_models.append(offspring)

        # mutate models
        next_generation_models = [mutate(model, force_mutation=True) for model in next_generation_models]

        self.models = next_generation_models

    def get_best_model_probility(self):
        x = self.models[0].seqprobs()
        return sorted(x.items(), key=itemgetter(1), reverse=True)

    def seqprobs(self):
        results = []
        for model in self.active_models:
            results.append(model.seqprobs())
        return results

    def get_all_model_probabilities(self):
        probs = self.seqprobs()
        result = []
        for d_instance in probs:
            result.append(sorted(d_instance.items(),
                                 key=itemgetter(1), reverse=True))
        return result
