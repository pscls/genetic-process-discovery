from base_files.mim import model, sortbyvalue
from operator import itemgetter

class ModelManager:

    inactive_models = []  # array of all models that are successfully estimated
    active_models = []  # number of all currently used models

    @staticmethod
    def create_models(symbol_sequence: str, number_of_models: int = 5):
        assert number_of_models > 0
        for _ in range(number_of_models):
            # TODO: Initaialize the matrices differently - currently default m+ init 
            ModelManager.active_models.append(model(symbol_sequence))

    @staticmethod
    def train_model(model):
        model.estparams()
        model.estsources()
        return

    @staticmethod
    def run(epochs=5):
        assert epochs > 0
        assert len(ModelManager.active_models) > 0

        while len(ModelManager.active_models) > 0 and epochs > 0:
            # Do one iteration for all models -> update Matrix with current symbol string
            # afterwards compute new symbol string from Matrix
            for model in ModelManager.active_models:
                ModelManager.train_model(model)

            # TODO: Start here with gentic programming
            # 1. find a way to rate each model and sort them by this rating

            # 2. Take model.s and do some stuf with it
            # Then overwrite model.y with y* which gets computed from model.s
            
            epochs -= 1
        return

    @staticmethod
    def get_best_model_probility():
        x = ModelManager.active_models[0].seqprobs()
        return sorted(x.items(),
                                key=itemgetter(1), reverse=True)

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